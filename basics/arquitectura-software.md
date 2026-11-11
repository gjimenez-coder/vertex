---
inclusion: manual
---

# Arquitectura de Software — Principios Reutilizables

> Alcance: principios de organización de código para aplicaciones de capas (típicamente backend modular), independientes de framework. Los ejemplos son ilustrativos; adáptalos al stack del proyecto.

La idea de fondo: **el orden importa más que las herramientas**, y **la simplicidad importa más que el orden**. Un código predecible se mantiene y escala; uno ad-hoc se degrada; uno sobreconstruido se vuelve inmanejable antes de que haga falta.

---

## 1. Separación de responsabilidades por capas

Define capas con un contrato de dependencia claro y respétalo sin excepciones:

- **Controller / Handler** — entrada (HTTP, eventos, jobs): valida, controla acceso, delega. No contiene lógica de negocio.
- **Service** — lógica de negocio y orquestación. Es el único punto de entrada a un módulo desde fuera.
- **Repository / Data Access** — acceso a datos. Solo queries, sin lógica de negocio.

Reglas de dirección de dependencias:

- Un módulo **solo llama al Service de otro módulo**, nunca a su Repository ni a su almacenamiento directamente.
- Un Service puede importar otros Services. Un Repository **nunca** importa otro Repository (ni siquiera para "unificarlos" en una fachada).
- Los handlers (eventos, jobs) **solo hablan con Services**, no con Repositories ni con la DB.

```
✅  await ordersService.updateItemPrices(tx, orderId, items)
❌  await db.update(orderItems).set(...)              // handler/service tocando la DB directamente
❌  await promotionsRepository.confirmReservations()  // saltándose el Service de otro módulo
```

> Esta es la única definición de estas reglas; `backend.md` las enlaza.

---

## 2. Transacciones y atomicidad

- Las transacciones se abren en la capa que **orquesta** (Service o Handler), nunca en el Repository.
- Los métodos de acceso a datos aceptan un ejecutor opcional (`executor = db` o `tx`) para poder participar en una transacción externa.
- Pasar la transacción hacia abajo garantiza atomicidad: todo hace commit o rollback junto.

Qué va dentro de la transacción y qué no (efectos externos): `backend.md` §2.

---

## 3. Estructura predecible de un módulo

Cada módulo sigue la misma forma, de modo que cualquiera sepa dónde buscar:

```
modules/foo/
  foo.controller.*   — entrada: endpoints, validación, control de acceso
  foo.service.*      — lógica de negocio, transacciones, orquestación
  foo.repository.*   — acceso a datos (solo queries)
  foo.schema.*       — definición de datos/tablas (SIN constantes de dominio)
  foo.constants.*    — constantes, enums y tipos derivados del módulo
  foo.types.*        — contratos: inputs, outputs, shapes de respuesta
  foo.helpers.*      — funciones puras (sin inyección, sin DB)
  handlers/          — manejadores de eventos
```

- **Crea cada archivo cuando hace falta**, no por plantilla: un módulo pequeño puede no tener `helpers` ni `types`. La estructura es el *lugar* donde va algo, no una obligación de llenarla.
- **Marca explícitamente qué es público y qué es privado.** Documenta los métodos públicos que no son para la capa de entrada (los que consume otro Service/Handler).
- Agrupa los métodos del Service por audiencia: API pública para controllers, API pública para otros módulos, y privados.

---

## 4. Cada cosa en su lugar

Nada de constantes, tipos o helpers "sueltos" en archivos que no les corresponden.

| Qué | Dónde vive | No debe estar en |
|---|---|---|
| Constantes y enums de dominio | `*.constants.*` | schema, service, controller, repository |
| Tipos de contrato (input/output/respuesta) | `*.types.*` | inline en service/controller |
| Tipos de la capa de datos (`Record`, `New`, `Patch`) | `*.repository.*` | — (re-exportables desde `*.types.*`) |
| Funciones puras del módulo (mapeos, transformaciones) | `*.helpers.*` | sueltas en el service |

```
✅  // foo.constants.*
    export const ORDER_STATUSES = ['pending', 'confirmed', 'cancelled'] as const;
❌  // suelto en el schema o el controller
    const MAX_SIZE = 5 * 1024 * 1024;
```

---

## 5. Cuándo nombrar un tipo

Un tipo de contrato merece nombre y archivo cuando:

- **cruza una frontera pública**: parámetro o retorno de un método que otro módulo o el controller consume; o
- **se reutiliza**: aparece en 2+ firmas; o
- **tiene más de un puñado de campos que viajan juntos** y se vuelve ilegible inline (como guía, ~4 o más).

Un objeto local de 2 o 3 campos que no sale del método puede quedarse inline. El umbral numérico es una guía de legibilidad, no una regla mecánica.

```
✅  async createFoo(input: CreateFooInput): Promise<FooResult>     // frontera pública
✅  const pair: { min: number; max: number } = ...                  // local, 2 campos
❌  async createFoo(input: { id; tenantId; name; category; isActive }): ...  // público, 5 campos
```

---

## 6. Regla de las dos apariciones (DRY con criterio)

Promueve a compartido cuando algo se repite, no antes:

- La misma **constante** en 2+ módulos → muévela a `shared/constants/`.
- La misma **función** en 2+ módulos → muévela a `shared/utils/`.
- El mismo **tipo genérico** (`PaginatedResult<T>`, `CursorPage<T>`) en 2+ módulos → muévelo a `shared/`.

Evita abstraer de forma prematura con una sola aparición; evita duplicar a partir de la segunda.

---

## 7. Configuración centralizada

Los valores de configuración (TTLs, límites, URLs) no se hardcodean: vienen de un servicio de configuración validado al arrancar. Regla y flujo completos en `backend.md` §6.

---

## 8. Comentarios con intención

- Comentarios **cortos y directos** que respondan: ¿qué toca? ¿persiste datos? ¿cuál es el objetivo? No narres lo obvio.
- En métodos largos, usa separadores de fase para marcar el flujo.

```
✅  /** Persiste precios en order_items. Requiere tx. */
❌  /** This method is responsible for updating the sale price after the discount... */

    // ── 1. Validar stock ──────────
    // ── 2. Aplicar descuentos ─────
    // ── 3. Persistir ──────────────
```

---

## 9. Servicios: cuándo dividir y cuándo no

**Empieza con un monolito modular.** Un solo desplegable con módulos bien separados da casi todo el beneficio de los servicios (fronteras claras, equipos por módulo) sin el costo de la red, las transacciones distribuidas y la operación de varios sistemas. Los microservicios no son una bala de plata: añaden fallos parciales, latencia, consistencia eventual y complejidad operativa.

Extrae un servicio **solo si** resuelve un problema medible y concreto:

- una parte necesita **escalar, desplegarse o fallar** de forma independiente al resto;
- hay un requisito **regulatorio o de seguridad** que exige aislamiento (por ejemplo, alcance de cumplimiento de pagos);
- un **equipo distinto** es dueño de esa capacidad y el acoplamiento lo frena.

Si el motivo es "se ve más ordenado" o "por si acaso crece", no extraigas.

Cuando extraigas:

- **Descompón por capacidad de negocio**, no por capa técnica. Un servicio de "base de datos" o "validaciones" es un monolito distribuido.
- **Cada servicio es dueño de sus datos.** Nada de tablas compartidas entre servicios; solo API o eventos.
- **Contrato mínimo y opaco**: el servicio no interpreta identificadores ajenos (recibe una referencia externa como string opaco).
- **No hay transacción distribuida (2PC).** Una operación entre servicios se modela como pasos con transacciones locales y compensaciones (`backend.md` §10).
- Protege el modelo de cada lado con una **capa anticorrupción**: traduce entre modelos en el borde, no dejes que el modelo ajeno contamine el tuyo.
- Migra de forma **incremental** (patrón strangler): nuevas funciones como servicio, extrae por capacidad, mantén el monolito funcionando. Evita la reescritura "big bang".

Antipatrón: el **monolito distribuido**, servicios que deben desplegarse juntos o que se llaman en cascada síncrona para cada petición.

---

## 10. Tamaño y cohesión

Un módulo que crece sin control se vuelve imposible de entender.

- Una clase o service debe tener **una razón para cambiar**. Si mezcla varios subdominios (por ejemplo precios, reservas y reportes), divídelo por subdominio.
- Señales de que hay que dividir: el archivo no cabe en la cabeza (como guía, más de ~500 líneas), nombres comodín (`Manager`, `Processor`, `Helper`), o muchos métodos privados que solo sirven a un subconjunto de los públicos.
- Las funciones hacen **una cosa y a un solo nivel de abstracción**; si necesitas separadores de fase (§8) en un método largo, probablemente son funciones distintas.
- Divide con **pasos pequeños verificados por tests** (ver `testing.md` §7), no con una reescritura.

---

## 11. Simplicidad: no escribas lo que no necesitas

- **No escribas código hasta que lo necesites.** No sabes cómo debe funcionar lo que aún no hace falta; casi siempre habrá que rediseñarlo, y mientras tanto se pudre.
- **Borra el código que no se usa**: stubs, módulos sin conectar, duplicados, campos "para el futuro". El historial de git los conserva.
- **Diseña con lo que sabes ahora**, no con predicciones. Mantén los cambios pequeños para que el diseño se pueda ajustar.
- **Sé solo tan genérico como sepas que necesitas ser hoy.** Un adaptador para un único proveedor, o una abstracción con una sola implementación, se justifican solo si hay un segundo caso concreto y cercano.
- Prefiere desarrollo y diseño **incrementales**: construye la pieza más simple, ajusta el diseño, repite.

```
✅  una interfaz con un adaptador cuando ya hay (o está acordado) un segundo proveedor
❌  framework de plugins "por si algún cliente quiere conectar otro sistema"
❌  campo `active` en la tabla sin ningún código que lo use
```

---

## Prohibido

- Que un handler o service acceda directamente a la DB o al Repository de otro módulo.
- Fachadas de Repositories (un Repository que importa otros).
- Abrir transacciones en el Repository.
- Constantes, enums o tipos sueltos fuera de su archivo.
- Tipos anónimos grandes en firmas públicas.
- Duplicar una constante/función/tipo que ya aparece en 2+ módulos.
- Extraer un servicio sin un problema medible, o compartir tablas entre servicios.
- Services que acumulan subdominios sin dividirse.
- Código muerto, stubs sin uso o abstracciones sin segundo caso.

---

## Checklist al crear o refactorizar un módulo

- [ ] ¿Las capas respetan la dirección de dependencias (Controller → Service → Repository)?
- [ ] ¿Los módulos se comunican solo vía Services?
- [ ] ¿Las transacciones se abren en el orquestador y se propagan hacia abajo?
- [ ] ¿Cada archivo del módulo existe porque hace falta, no por plantilla?
- [ ] ¿Los métodos tienen el modificador de acceso correcto y están agrupados por audiencia?
- [ ] ¿Las constantes/enums están en `*.constants.*`, no sueltos?
- [ ] ¿Los tipos que cruzan fronteras o se reutilizan están en `*.types.*`?
- [ ] ¿Lo que aparece en 2+ módulos se movió a `shared/`?
- [ ] ¿El service tiene una sola razón de cambio y un tamaño que se pueda leer?
- [ ] ¿Se borró el código que no se usa y no se escribió lo que aún no hace falta?
- [ ] Si se propone un servicio nuevo: ¿hay un problema medible que lo justifique?

---

## Cuándo aplicar

- **Siempre / hoy (nivel 1):** capas y dirección de dependencias, transacciones en el orquestador, cada cosa en su lugar, regla de las dos apariciones, YAGNI y borrar código muerto, monolito modular como punto de partida. Dividir un service por subdominio cuando deja de caber en la cabeza.
- **Al crecer (nivel 2):** señales de tamaño más estrictas cuando entra una segunda persona (el archivo ya no lo entiende quien no lo escribió); estructura de módulo más rigurosa para facilitar el trabajo en paralelo.
- **Con varios servicios o equipos (nivel 3):** criterios de extracción medibles, capa anticorrupción, un dueño de datos por servicio, ausencia de 2PC. Antes de ese punto, un segundo servicio solo se justifica por un requisito de aislamiento o cumplimiento, no por orden.
