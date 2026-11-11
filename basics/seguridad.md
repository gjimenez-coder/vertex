---
inclusion: manual
---

# Seguridad — Principios Reutilizables

> Alcance: principios de seguridad para aplicaciones web (frontend + backend), independientes de framework. Los ejemplos son ilustrativos; adáptalos al stack del proyecto.

Estos principios se destilaron de proyectos reales y de la literatura de seguridad web. La regla es el activo; la implementación concreta se re-ancla en cada proyecto. Piensa siempre en el **peor caso**: cada función se evalúa por cómo puede abusarla un usuario malintencionado, un script interno o un token comprometido, no solo por el uso previsto.

---

## 1. Tokens y sesión

- El token de sesión (JWT u otro) **nunca debe vivir en JavaScript accesible**. Viaja como cookie `HttpOnly; Secure; SameSite=Strict` seteada por el servidor.
- El cliente guarda en storage solo **metadatos no sensibles** (nombre, permisos, config). Nunca el token.
- **Nunca uses `localStorage` para tokens.** Si necesitas persistir algo entre sesiones, persiste solo un ID opaco.
- Verifica la sesión contra el servidor al arrancar la app (endpoint tipo `GET /me`) para restaurar permisos frescos, en vez de confiar en lo que haya en el cliente.

```
✅  credentials: 'include'            // la cookie HttpOnly la adjunta el browser
❌  Authorization: `Bearer ${token}`  // token expuesto en JS (salvo casos puntuales como impersonation)
❌  localStorage.setItem('token', jwt)
```

- Usa **access token de TTL corto** (ej. 15 min) + **refresh token de TTL largo** (ej. 7 días) en cookie restringida por `path` a los endpoints de auth.
- Ante un `401`, intenta refrescar automáticamente una vez; si falla, limpia la sesión y fuerza re-login.
- Los IDs de sesión son largos, aleatorios (PRNG criptográfico), se renuevan al autenticar y **nunca** viajan en la URL.
- Las contraseñas se guardan con hash fuerte y salt; nunca se envían por email. Limita los intentos de login por cuenta **y** por origen.

---

## 2. CSRF

- Toda **mutación** (POST/PUT/PATCH/DELETE) debe protegerse contra CSRF.
- Patrón recomendado: **double-submit cookie**. El servidor emite un token CSRF en una cookie legible por JS; el cliente lo reenvía en un header (`X-CSRF-Token`) que el servidor valida.
- `SameSite=Strict` mitiga la mayoría de los casos, pero el token CSRF es la **segunda capa** — no te quedes solo con uno.
- Centraliza el envío del header en el cliente HTTP, no lo agregues manualmente en cada llamada.

---

## 3. Control de acceso

- **Defensa en dos capas:** una guard de layout (redirige si no hay sesión) **y** una verificación de permiso específico por ruta/acción. Ninguna ruta autenticada debe quedar fuera de la primera capa.
- **El cliente nunca es la autoridad.** El control de acceso del frontend es UX; la decisión real se toma y se re-valida **siempre en el servidor**.
- Aplica **menor privilegio**: cada acción exige el permiso mínimo necesario, no un rol genérico. Esto incluye tokens de servicio y scripts internos: un job que solo agrega puntajes no necesita escribir en toda la tabla.

```
✅  <RequireAuth permission="catalog.view"><Page/></RequireAuth>
❌  <Page/>   // ruta autenticada sin guard
```

---

## 4. Secretos y datos en el cliente

- Asume que **todo lo que llega al bundle del cliente es público**. No metas secretos en variables de build del frontend; úsalas solo para valores no sensibles (ej. URL pública de la API).
- Prefiere un **dominio público estable** para la API, no la URL interna de infraestructura.

> Los secretos del servidor y la config (TTLs, límites) se definen en `backend.md` §6 y `seguridad.md` §13. No se repiten aquí.

---

## 5. Logging seguro

- **Nunca `console.*` directo en producción.** Usa un logger que decida qué emitir según el entorno.
- En producción, los mensajes deben ser **claves opacas** sin stack traces, nombres de módulos internos ni datos sensibles. En desarrollo, contexto completo.

```
✅  logger.warn('audit_permission_denied')
❌  console.warn('[AuditContext] El usuario no tiene permiso audit.view')
```

- No registres tokens, credenciales, PII ni datos de tarjeta en texto plano, ni siquiera en estructuras inspeccionables desde el cliente (ej. `dataLayer` de analytics). Redacta en el logger los campos sensibles conocidos.
- Los procesos automáticos registran autoría explícita (`'system'`): ver `backend.md` §4.

---

## 6. Security headers y CSP

- Mantén headers de seguridad mínimos en toda app web:
  - `Content-Security-Policy` (ver abajo)
  - `Strict-Transport-Security` (HSTS): `max-age` largo e `includeSubDomains`. Prefiérelo a los redirects 301, que dejan una primera petición HTTP vulnerable.
  - `frame-ancestors 'none'` vía CSP (`X-Frame-Options: DENY` es su equivalente legado; mantenlo solo por compatibilidad).
  - `X-Content-Type-Options: nosniff`
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Permissions-Policy` restringiendo APIs que no uses (cámara, micrófono, geolocalización…)
- **Despliega la CSP en modo `Report-Only` primero.** Pásala a enforce solo tras verificar que no hay violaciones legítimas.
- **Define el criterio de salida del Report-Only**: un periodo sin violaciones legítimas (ej. 2 semanas de tráfico real) y una fecha de revisión. Un `Report-Only` que nunca se revisa no protege nada.
- Prefiere una CSP estricta: sin `unsafe-inline` ni `unsafe-eval` en scripts; con nonce (páginas renderizadas en el servidor) o hash (apps estáticas cacheadas).
- Al integrar un dominio externo nuevo (CDN, fonts, API), agrega su directiva explícita a la CSP en vez de abrirla con comodines.
- Quita los headers que revelan versiones (`X-Powered-By`).

---

## 7. Validación y confianza de datos

- **Valida en el borde antes de confiar.** Todo input que cruza una frontera de confianza (formulario → API, API → DB) se valida contra un esquema explícito.
- La validación del cliente es para UX (feedback rápido); **no sustituye** la validación del servidor, que es la autoritativa.
- Los tipos/esquemas del cliente deben **reflejar fielmente** los contratos del servidor: lo requerido en el servidor es requerido en el cliente.
- **Todo body pasa por un esquema.** Un `@Body()` sin validación es un hueco aunque el resto del módulo valide.

---

## 8. Mass assignment y autorización por objeto (IDOR)

### Mass assignment

Nunca actualices campos a partir de un objeto que el cliente controla sin filtrarlo.

- Usa **allowlist de campos** o un esquema/DTO **estricto** que rechace campos extra (`.strict()` en DTOs públicos).
- Campos que el cliente no debe decidir (precios, roles, tenant, estado, autoría) **se resuelven en el servidor**, no se aceptan del body.

```
✅  schema.strict()           // un campo `price` o `isAdmin` enviado por el cliente se rechaza
❌  db.update(id, req.body)   // el cliente decide qué columnas cambian
```

### Autorización por objeto (IDOR)

Poseer una URL o un ID no es tener permiso.

- Verifica en **cada petición** que el usuario puede acceder a **ese objeto** (propiedad, tenant, unidad), no solo que tiene el rol.
- Si el llamante no está autorizado a ver un recurso, responde **como si no existiera** (`404`, no `403`): evita revelar qué existe.
- No expongas IDs secuenciales en URLs; usa identificadores aleatorios. Esto disuade el sondeo pero **no reemplaza** la verificación de autorización.
- Los nombres de archivo que sube el usuario **nunca** forman parte de una ruta: guárdalos como dato y genera una clave aleatoria para el archivo (evita directory traversal).

---

## 9. XSS

- Trata todo dato de usuario como **texto**, no como HTML. El framework de UI escapa por defecto; no lo desactives.
- **Evita los sinks peligrosos**: `innerHTML`, `outerHTML`, `document.write`, `dangerouslySetInnerHTML`, `eval`. Si necesitas HTML enriquecido, sanéalo con una librería auditada y una allowlist de etiquetas.
- **Sanea al entrar y escapa al salir.**
- Los datos que vienen de una base de datos pueden haberse originado en un usuario: aplican las mismas reglas.
- Los enlaces con `target="_blank"` llevan `rel="noopener noreferrer"` (evita que la página abierta controle la original: tabnabbing).
- Valida las URLs que vienen de usuarios (`https:` y dominios esperados); nunca `javascript:` ni redirecciones abiertas.
- La CSP estricta (§6) es la segunda línea de defensa, no la primera.

```
✅  <p>{user.bio}</p>
❌  <p dangerouslySetInnerHTML={{ __html: user.bio }} />
❌  <a href={user.website} target="_blank">   // sin noopener y sin validar el esquema
```

---

## 10. Inyección

- **Nunca concatenes entrada de usuario** en SQL, comandos de shell, expresiones de búsqueda ni consultas de otro motor. Usa **queries parametrizadas** (placeholders) o el query builder del ORM.
- En SQL crudo, interpola solo valores como parámetros, jamás identificadores o fragmentos del cliente. Si un nombre de columna u orden viene del cliente, valídalo contra una allowlist.
- No ejecutes comandos de shell con entrada de usuario; si es inevitable, usa la forma de arreglo de argumentos y valida contra allowlist.
- Si procesas XML, deshabilita las entidades externas y DTD del parser; mejor aún, usa JSON.
- Aplica mínimo privilegio a la cuenta de base de datos de la aplicación (sin permisos de DDL ni de superusuario).

```
✅  db.execute(sql`SELECT * FROM users WHERE email = ${email}`)   // parámetro
❌  db.execute(`SELECT * FROM users WHERE email = '${email}'`)    // concatenación
```

---

## 11. Enumeración y exposición de PII

La enumeración es filtrar datos pequeños, repetidamente, hasta reconstruir algo que no se debía exponer.

- **Mensajes de autenticación genéricos**: un solo mensaje ("credenciales inválidas") para usuario inexistente, contraseña incorrecta o cuenta bloqueada. Lo mismo para "olvidé mi contraseña": responde igual exista o no la cuenta.
- **Códigos y mensajes de error con allowlist**: no reflejes errores crudos del servidor ni de la base de datos; devuelve el mensaje genérico más cercano.
- **Rate limit en todo endpoint enumerable** (login, búsquedas por email o teléfono, verificación de códigos, lookup de pedidos por código). Fija el límite en el borde superior del uso legítimo.
- **IDs y códigos no secuenciales ni predecibles** (nada de IDs por orden de alta; los códigos de seguimiento tienen suficiente entropía).
- **No devuelvas datos personales por búsquedas públicas** (por teléfono, email o documento). Si el producto necesita autocompletar (por ejemplo en un checkout), limita lo que se devuelve (lo mínimo, sin dirección ni documento), exige verificación del titular y aplica rate limit estricto.

```
✅  GET /lookup?phone=… → { exists: true }        // nada más, con rate limit y verificación
❌  GET /customers/by-phone/:phone → nombre, dirección, documento   // público y sin límite
```

---

## 12. CORS y cookies

### CORS

- Configura una **allowlist de orígenes concretos**. Nunca `*`, y **nunca refleje cualquier origen** (`origin: true`) junto con `credentials: true`.
- Valida la configuración al arrancar: en producción un origen comodín debe fallar el arranque, no solo advertir.
- Restringe métodos y headers a los que la API usa. Aplica el menor alcance posible.

### Cookies

- Atributos: `Secure`, `HttpOnly`, `SameSite=Strict` (o `Lax` si el flujo lo exige) y `Path` lo más acotado posible.
- **Evita el atributo `Domain`.** Con `Domain=.ejemplo.com` la cookie se envía a todos los subdominios; si alguno sirve contenido de terceros o de tenants (por ejemplo tiendas por subdominio), un XSS ahí compromete la sesión del panel.
- Si necesitas compartir sesión entre subdominios, hazlo de forma explícita y aísla los orígenes que sirven contenido de usuarios en otro dominio.

---

## 13. Secretos y credenciales

- Los secretos (claves de API, contraseñas de base de datos, claves de firma) viven en un **gestor de secretos** (Secret Manager, Vault, KMS) y se inyectan al entorno al desplegar. Nunca en el repo, en el artefacto de build ni en una variable de texto plano versionada.
- **No los guardes en el estado de infraestructura como código** sin protegerlo: ese archivo suele contener los valores en claro. Cifra el backend de estado y restringe quién lo lee.
- **Rota** los secretos con un calendario y de inmediato ante una sospecha de filtración. Diseña para poder rotar sin redeploy manual.
- Una credencial por propósito y por entorno; permisos mínimos. Los archivos de credenciales solo son legibles por el usuario de la aplicación.
- No imprimas secretos en logs ni en dumps de memoria; desactiva los core dumps en producción.
- Detecta secretos accidentales en el repo con un escáner en CI (ver `cicd.md` §2).

---

## 14. Dependencias

Cada dependencia trae sus propias dependencias; el árbol completo puede tener miles de paquetes.

- **Fija versiones**: lockfile versionado y `install` congelado en CI (`--frozen-lockfile` o `npm ci`). Un build no debe actualizar dependencias por sí solo.
- **Audita el árbol completo** (no solo las dependencias directas) contra bases de CVE de forma **automatizada** en CI y de forma periódica. Revisa cada versión única, no solo cada paquete.
- Actualiza con regularidad parches de seguridad; la mayoría de los ataques usan vulnerabilidades conocidas y sin parchear.
- **Menos es más**: antes de añadir una dependencia, evalúa su mantenimiento y tamaño; elimina las que no usas.
- Aísla las dependencias de mayor riesgo (procesamiento de archivos, parsers de formatos complejos) con el mínimo privilegio.
- Ejecuta procesos y contenedores **sin root**, con imágenes base mínimas que se reconstruyen con regularidad.

---

## 15. Datos de pago

Si la aplicación toca pagos con tarjeta, reduce el alcance de cumplimiento (PCI) en lugar de asumirlo:

- **Nunca almacenes** CVV/CVC, PIN ni datos de banda completos; el PAN solo enmascarado (como mucho primeros 6 y últimos 4 dígitos).
- Usa formularios alojados o tokenización de la pasarela para que los datos de tarjeta **no pasen por tus servidores**.
- Redacta campos de tarjeta en logs y en payloads guardados de webhooks.

---

## 16. DoS y límites

La denegación de servicio es una cuestión de grado: cualquier funcionalidad que consume recursos sin límite es un riesgo.

- **Límite de tamaño de body por ruta**: bajo por defecto, alto solo en las rutas que lo necesitan. Un límite global alto expone a los endpoints públicos.
- **Rate limit por tipo de endpoint** (auth, checkout, búsquedas, subidas), y en el borde antes de llegar a la aplicación cuando sea posible.
- **Nunca aceptes expresiones regulares del usuario**, y revisa las propias en busca de backtracking catastrófico (grupos repetidos anidados como `(a+)+`).
- Limita la complejidad de las consultas: paginación con máximo, profundidad y tiempo máximo de cómputo para consultas complejas, y timeouts de statement en la base de datos.
- Registra los tiempos de respuesta de peticiones **y de jobs asíncronos**: sin observabilidad no se detecta el abuso (ver `observabilidad.md`).
- Las mitigaciones agresivas pueden bloquear usuarios legítimos: mide primero el uso normal antes de fijar umbrales. (Resiliencia ante carga: `manejo-errores.md` §7.)

---

## Prohibido

- Guardar tokens en `localStorage`/`sessionStorage`.
- Confiar en el control de acceso del cliente como única barrera.
- Secretos, TTLs o URLs internas hardcodeados; secretos en repo, estado de IaC o artefactos.
- `console.*` con detalles internos en producción.
- CSP en modo enforce sin haber pasado por report-only, o report-only sin criterio de salida.
- Mutaciones sin protección CSRF.
- Mensajes de error en producción que filtren estructura interna.
- `db.update(id, body)` con el body completo del cliente.
- Autorizar solo por rol sin verificar el objeto.
- `innerHTML`/`dangerouslySetInnerHTML` con datos de usuario sin sanear.
- SQL por concatenación; regex suministradas por el usuario.
- CORS con `*` o reflejando cualquier origen con credenciales.
- Atributo `Domain` en cookies de sesión sin necesidad probada.
- Mensajes de auth que distinguen usuario inexistente de contraseña errónea.
- Búsquedas públicas que devuelven PII sin verificación ni rate limit.
- Dependencias sin lockfile o sin auditoría de CVE.

---

## Checklist

- [ ] ¿El token de sesión viaja en cookie `HttpOnly; Secure; SameSite`, fuera de JS y nunca en la URL?
- [ ] ¿Las mutaciones adjuntan y el servidor valida el token CSRF?
- [ ] ¿Hay refresh con TTL corto para el access token?
- [ ] ¿El control de acceso está en dos capas, es por objeto y se re-valida en el servidor?
- [ ] ¿Cada acción, token y job exige el permiso mínimo?
- [ ] ¿No hay secretos ni URLs internas en el código, el repo, el artefacto ni el estado de IaC?
- [ ] ¿El logging de producción usa claves opacas, sin datos sensibles ni stack traces?
- [ ] ¿Están los security headers (incluido HSTS) y la CSP, con criterio de salida del report-only?
- [ ] ¿Todo body pasa por un esquema estricto y no acepta campos que el cliente no debe decidir?
- [ ] ¿No hay sinks de XSS con datos de usuario y los `target="_blank"` llevan `noopener`?
- [ ] ¿Todas las queries son parametrizadas?
- [ ] ¿Los mensajes de auth son genéricos y los endpoints enumerables tienen rate limit?
- [ ] ¿Ninguna búsqueda pública devuelve PII sin verificación?
- [ ] ¿CORS usa allowlist de orígenes y las cookies evitan `Domain`?
- [ ] ¿Las dependencias están fijadas y auditadas automáticamente?
- [ ] ¿Hay límites de body por ruta, rate limits y tiempos máximos de consulta?

---

## Cuándo aplicar

- **Siempre / hoy (nivel 1):** sesión por cookie `HttpOnly`, CSRF, control de acceso por objeto, validación estricta de todo body, XSS e inyección (parametrizar), mensajes de auth genéricos, rate limit en auth y en endpoints públicos que devuelven datos, CORS con allowlist, secretos fuera del repo y del estado de IaC, lockfile congelado y auditoría de CVE en CI, límite de body por ruta, no almacenar datos de tarjeta. Todo esto es barato y evita los incidentes más caros.
- **Al crecer (nivel 2):** gestor de secretos con rotación calendarizada, CSP en enforce con nonce o hash, HSTS con `includeSubDomains`, escáner de secretos y de dependencias como gate de merge, rate limit en el borde (WAF/CDN), revisión de código con checklist de seguridad.
- **Con varios servicios o equipos (nivel 3):** modelo de amenazas por feature expuesta (actores, vectores, mitigaciones y delta), autenticación servicio a servicio, auditoría inalterable de accesos privilegiados, pruebas de penetración periódicas y proceso formal de gestión de vulnerabilidades.
