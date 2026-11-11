---
inclusion: manual
---

# Manejo de Errores y Resiliencia — Principios Reutilizables

> Alcance: cómo representar, propagar, registrar y recuperar errores en aplicaciones cliente-servidor, y cómo evitar que una falla se propague. Independiente de lenguaje. Complementa `apis.md` (errores HTTP), `seguridad.md` (logging seguro) y `observabilidad.md`.

Premisa: **las fallas son inevitables.** No se trata de eliminarlas todas, sino de diseñar lo que pasa *después* de que aparece la primera grieta.

---

## 1. Falla rápido y explícito

- Valida precondiciones y entradas **al borde**, antes de ejecutar lógica, y rechaza temprano. (Ver `backend.md` §7, `apis.md`.)
- Un error nunca debe pasar silencioso: o se maneja, o se propaga, pero nunca se ignora.

```
✅  if (!order) throw new NotFoundError({ code: 'order_not_found', orderId })
❌  const order = await find(id)   // si es null, el bug aparece 10 líneas después
```

---

## 2. Errores tipados con código semántico

- Representa los errores de dominio como **tipos/excepciones con un `code` estable** (snake_case), no como strings genéricos ni `Error` base.
- El `code` lo consume el cliente **programáticamente**; el `message` es para humanos; `details` opcional para debugging. (Estructura HTTP: `apis.md` §3.)
- Distingue **errores esperados** (de dominio: stock insuficiente, no autorizado) de **errores inesperados** (bugs, fallos de infraestructura). Se tratan distinto.

```
✅  throw new ConflictError({ code: 'token_already_revoked', message: '...' })
❌  throw new Error('something went wrong')
```

---

## 3. Esperado vs. inesperado

| | Esperado (de dominio) | Inesperado (bug / infra) |
|---|---|---|
| Ejemplos | validación, no autorizado, conflicto | null deref, timeout de DB, OOM |
| Log | `warn` / `info` | `error` con stack y contexto |
| Respuesta al cliente | código y mensaje accionable | mensaje opaco genérico + `requestId` |
| Alerta | normalmente no | sí (ver `observabilidad.md`) |

Nunca filtres detalles internos (stack traces, nombres de módulos, SQL) al cliente en producción. (Ver `seguridad.md` §11.)

---

## 4. Maneja el error en la capa correcta

- No atrapes un error solo para re-lanzarlo igual. Captura donde **puedes hacer algo**: traducirlo a un error de dominio, agregar contexto, o decidir una recuperación.
- Al envolver un error, **preserva la causa original** (encadenamiento) para no perder el rastro.
- Centraliza la traducción final a respuesta (un filtro/handler global de errores HTTP) en vez de repetir el mapeo en cada endpoint.

```
✅  catch (e) { throw new DomainError({ code: 'payment_failed', cause: e }) }
❌  catch (e) { throw e }            // captura inútil
❌  catch (e) { throw new Error(e.message) }  // pierde el stack original
```

---

## 5. Reintentos, timeouts y degradación

- **Reintentos** solo para fallos transitorios (red, 5xx, timeouts), con **backoff exponencial + jitter** y un máximo. Nunca reintentes errores de dominio (un 400 no mejora al repetirlo).
- Reintentar de inmediato casi siempre vuelve a fallar: prefiere **encolar y reintentar más tarde** (store-and-forward) a hacer esperar al usuario.
- Las operaciones con efectos que se reintentan deben ser **idempotentes** (ver `apis.md` §4, `backend.md` §3).
- **Timeouts**: toda llamada saliente tiene timeout (ver §7).
- Define el comportamiento de **degradación**: ¿qué hace el sistema si una dependencia no esencial cae? (fallback, valor por defecto, feature off).

---

## 6. El usuario recibe algo accionable

- Mensaje claro en su idioma, que diga qué pasó y qué puede hacer. Nada de "Error 500" a secas ni volcados técnicos.
- Preserva el trabajo del usuario ante un error (no borres el formulario); permite reintentar.

---

## 7. Resiliencia: que una grieta no se vuelva una caída

### Timeouts en toda llamada saliente

Una respuesta lenta es **peor que un error**: ata el hilo, la conexión y la capacidad de ambos lados. Un punto de integración sin timeout es la forma más común de caer en cascada.

- **Todo** llamado a otro servicio, API de tercero, base de datos, cola o SDK tiene timeout explícito (de conexión y de lectura). No asumas que el SDK trae uno razonable.
- Todo pool que bloquea hilos o conexiones tiene timeout de espera.
- Trata la respuesta de un tercero como **datos no confiables** hasta validarla (formato, tipo, esquema).

```
✅  fetch(url, { signal: AbortSignal.timeout(config.thirdPartyTimeoutMs) })
❌  fetch(url)   // puede colgar para siempre
```

### Fail Fast

- Si puedes saber de antemano que la petición va a fallar (recurso no disponible, parámetro inválido, breaker abierto), falla de inmediato, antes de gastar trabajo.
- Distingue **falla de sistema** (503, recurso no disponible) de **falla de aplicación** (400, datos inválidos): quien llama no debe abrir su circuit breaker por datos erróneos de un usuario.

### Límites en todo lo que crece

- **Resultados**: toda consulta lleva `LIMIT`. Un result set sin límite puede devolver millones de filas de golpe. No confíes en que la tabla "siempre será chica" ni en que los productores de datos se portan bien.
- **Colas**: acotadas. Una cola sin límite consume la memoria hasta caer; con un límite lleno rechaza o frena al productor.
- **Cachés**: con tamaño máximo y política de invalidación o expiración.

### Steady State: lo que se acumula se purga

Para cada recurso que crece (datos, logs, archivos temporales, caché) debe existir un mecanismo que lo recicle.

- Define **retención** para tablas de eventos, outbox, auditorías operativas, carritos y sesiones. La purga la hace la lógica de la aplicación para respetar integridad referencial.
- Rota los logs y sácalos pronto a un destino central.
- Respeta la retención **legal** donde aplique (comprobantes fiscales): la purga no puede borrar lo que la ley obliga a conservar.
- Evita la intervención manual rutinaria en producción: cada mano es una oportunidad de error.

### Shed Load y Back Pressure

El mundo siempre puede generar más carga de la que puedes procesar.

- En los **bordes expuestos a internet**: rechaza trabajo nuevo cuando la capacidad está saturada (semáforo de concurrentes, rate limit) con `503`/`429` y `Retry-After`, en vez de aceptar y colapsar.
- **Dentro del sistema**: usa colas finitas para que el productor se frene (back pressure) en lugar de acumular.
- Cuando se active, el monitoreo debe enterarse (ver `observabilidad.md`).

### Bulkheads

Aísla capacidad para que una parte no tumbe al resto: pools de conexión o hilos separados por dependencia o por tipo de tráfico, límites de concurrencia por tenant o por función, y trabajos pesados fuera del proceso que atiende las peticiones interactivas.

### Circuit Breaker

Envuelve las llamadas a una dependencia que puede fallar de forma sostenida.

- Estados: **cerrado** (opera), **abierto** (falla de inmediato sin llamar), **semiabierto** (deja pasar una prueba tras un tiempo).
- Mide la **densidad** de fallas (cinco fallas en 30 segundos no son cinco en cinco horas), no el conteo total.
- Define con negocio el **fallback** (último valor bueno, valor en caché, respuesta degradada, encolar).
- Expón los cambios de estado al monitoreo y permite a operaciones abrirlo o resetearlo.

### Dogpile y automatización

- **Dogpile**: la carga de arranque o de un cron sincronizado puede superar a la de estado estable (cachés frías, todos los jobs a medianoche). Añade **jitter** aleatorio a crons, reintentos y arranques.
- **Governor**: la automatización (autoscaling, limpieza, reintentos masivos) actúa rápido y sin juicio. Limita su velocidad en la dirección peligrosa (apagar, borrar, bloquear), exige confirmación ante grandes discrepancias y da tiempo a que un humano intervenga.

### Antipatrones a evitar

- **Integration Point sin timeout**, la fuente número uno de caídas.
- **Cascada**: A espera a B que espera a C, todo síncrono, sin límites.
- **Reintento inmediato** y masivo contra un proveedor ya lento.
- **Result set sin límite**.
- **Capacidades desbalanceadas**: un front con mil hilos contra un backend con diez.

---

## Prohibido

- Tragar errores en silencio (`catch {}` vacío).
- `throw new Error('string')` para errores de dominio en vez de tipos con código.
- Filtrar stack traces o detalles internos al cliente en producción.
- Reintentar errores no transitorios o reintentar sin límite, backoff y jitter.
- Llamadas a servicios externos (incluidos SDKs) sin timeout.
- Perder la causa original al envolver un error.
- Queries, colas o cachés sin límite.
- Crons y reintentos sincronizados sin jitter.
- Purgas que ignoran la retención legal; acumulación sin política de retención.

---

## Checklist

- [ ] ¿Se valida y falla temprano en el borde?
- [ ] ¿Los errores de dominio son tipos con `code` estable, no strings?
- [ ] ¿Se distingue esperado vs. inesperado (log, respuesta, alerta)?
- [ ] ¿El cliente recibe mensaje opaco en producción, sin detalles internos?
- [ ] ¿Se captura solo donde se puede actuar, preservando la causa?
- [ ] ¿La traducción a respuesta HTTP está centralizada?
- [ ] ¿Los reintentos son solo para fallos transitorios, con backoff, jitter y límite?
- [ ] ¿Toda llamada saliente tiene timeout, incluido el SDK de terceros?
- [ ] ¿Las consultas, colas y cachés tienen límite?
- [ ] ¿Cada recurso que se acumula tiene política de retención o purga?
- [ ] ¿Los bordes públicos rechazan con 503/429 al saturarse?
- [ ] ¿Los crons y reintentos llevan jitter?
- [ ] ¿El usuario recibe un mensaje accionable y conserva su trabajo?

---

## Cuándo aplicar

- **Siempre / hoy (nivel 1):** errores tipados con `code`, esperado vs. inesperado, **timeouts en toda llamada saliente**, reintentos acotados con backoff y jitter, `LIMIT` en toda consulta, colas y cachés acotadas, retención de datos que se acumulan, jitter en crons, semáforo o rate limit en los endpoints públicos que consumen recursos. Todo es barato y evita las caídas en cascada más comunes.
- **Al crecer (nivel 2):** fallbacks de degradación acordados con negocio, aislamiento de trabajo pesado fuera del proceso que atiende peticiones interactivas, alertas sobre saturación y rechazos.
- **Con varios servicios o equipos (nivel 3):** circuit breaker por dependencia con estados observables, bulkheads (pools y límites por dependencia o tenant), back pressure entre servicios con colas finitas, governor sobre la automatización. Antes de ese punto, un circuit breaker completo suele ser más complejidad que valor; los timeouts y los reintentos acotados dan la mayor parte de la protección.
