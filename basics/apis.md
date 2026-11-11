---
inclusion: manual
---

# Diseño de APIs HTTP — Principios Reutilizables

> Alcance: diseño de APIs REST/HTTP, independiente de framework. Los ejemplos son ilustrativos. Complementa `seguridad.md`, `manejo-errores.md` y `backend.md`.

---

## 1. Recursos y verbos

- Las URLs identifican **recursos** (sustantivos), nunca acciones: `/orders`, no `/createOrder`.
- Plural para colecciones; kebab-case y minúsculas: `/business-units`, no `/businessUnits` ni `/business_units`.
- No anides más de dos niveles. `/tenants/:id/units/:unitId` está bien; más profundo → rediseña.
- Las acciones de dominio que no encajan en CRUD van como **sub-recurso con `POST`**.

```
✅  POST /orders/:id/cancel        POST /tokens/:id/rotate
❌  POST /cancelOrder              GET /orders/:id/delete
```

---

## 2. Verbos y códigos de estado

| Caso | Verbo | Código |
|---|---|---|
| Leer colección o recurso | `GET` | `200` |
| Crear (servidor genera ID) | `POST` | `201` |
| Reemplazar recurso completo | `PUT` | `200` |
| Modificar campos parciales | `PATCH` | `200` |
| Borrar / revocar sin body | `DELETE` | `204` |
| Borrar y devolver el recurso actualizado | `DELETE` | `200` |
| Acción de dominio con efectos | `POST` sub-recurso | `200`/`201` |
| Subir/reemplazar archivo existente | `POST` | `200` (no es creación) |
| Procesamiento diferido real | `POST` | `202` |

- Ante la duda entre `PUT` y `PATCH`, usa `PATCH`: más seguro contra el bug de "campo omitido se borra".
- `202 Accepted` **solo** cuando el efecto genuinamente aún no ocurrió (jobs async). Si el servidor completó el trabajo antes de responder (por ejemplo envió el email), es `200`/`201`, no `202`.
- Un `DELETE` **sin body** devuelve `204`. Si el cliente necesita el recurso resultante (por ejemplo la lista de imágenes tras borrar una), devuelve `200` con ese recurso; no mezcles ambos en el mismo endpoint.
- Subir un archivo a un recurso existente → `200`, no `201`. Añadir un elemento nuevo a una colección → `201`.
- Un input inválido es `400` (o `422`), no `409`. `409` es para conflictos de estado.

---

## 3. Errores consistentes

**Nunca `200 OK` con `{ "error": "..." }` en el body** — rompe middleware, alertas y circuit breakers. Devuelve siempre el código HTTP correcto y una estructura de error uniforme:

```json
{ "error": { "code": "insufficient_stock", "message": "...", "details": { } } }
```

- `code` en snake_case: el cliente lo maneja **programáticamente**.
- `message` en el idioma del usuario.
- `details` opcional, con contexto para debugging.
- Los errores inesperados devuelven un mensaje opaco y un `requestId` (ver `manejo-errores.md` §3).

```
✅  throw ConflictException({ code: 'token_already_revoked', message: '...' })
❌  throw new Error('Unsupported file type')   // genérico, sin código
```

**Un solo punto traduce excepciones a esta forma** (un filtro/handler global), no cada endpoint.

> **Nota de transición:** el formato canónico es el anidado. Si un servicio hoy responde el formato plano `{ code, message }`, los clientes deben tolerar ambos (`body.error?.code ?? body.code`) hasta que el filtro se alinee. No inventes un tercer formato.

---

## 4. Idempotencia y retries

Todo cliente serio reintenta ante fallo de red. Si un `POST` tiene efectos, debe tolerar retries sin duplicarlos.

- **Si el cliente envía el ID**, ese ID es el idempotency key: el ID duplicado se maneja con un conflicto diferenciado, nunca un `500`.
- Para operaciones sin ID de cliente, considera un header `Idempotency-Key: {uuid}` y cachea la respuesta por key durante un TTL corto. Misma clave con otro cuerpo → `409`.

---

## 5. Seguridad multi-tenant

- **Nunca confíes en headers del cliente** (`X-Tenant-Id`, etc.) para autorización; a lo sumo son hint de routing.
- El identificador de tenant/organización se valida **contra el token** en el guard, no contra el path param.
- Tokens, passwords y PII **nunca** en query params: se logean en proxies, CDNs e historial del navegador.
- Un filtro opcional por unidad (`?businessUnitId=`) también se valida contra los permisos del token.

```
✅  assertAccess(req.user, resourceOrgId)      // valida contra el token
❌  service.getData(req.headers['x-tenant-id']) // confía en el header
```

> Autorización por objeto, enumeración y PII: `seguridad.md` §8 y §11.

---

## 6. Paginación

- Toda colección que pueda crecer sin límite debe paginar. Nunca devuelvas colecciones sin `limit` (máximo razonable, ej. 100).
- Prefiere **cursor-based** sobre offset en tablas grandes (`OFFSET 10000` lee y descarta 10k filas).
- `sort` por query param: `?sort=created_at` (asc) / `?sort=-created_at` (desc).
- Una colección acotada y pequeña (catálogos de decenas de elementos) puede devolverse completa; documenta que es intencional.

```
GET /orders?cursor=abc123&limit=50     → { data: [...], nextCursor: "xyz" | null }
GET /units?page=1&limit=50             → offset solo para colecciones acotadas
```

---

## 7. Filtrado — siempre server-side

**Todo filtro de una lista se aplica en el backend**, nunca en el cliente. El frontend envía criterios como query params y el servidor filtra en SQL.

Por qué: el filtrado en el cliente solo ve la página ya descargada (da "sin resultados" aunque existan), no escala, y debe combinarse con la paginación y el orden que ya viven en el backend.

```
✅  GET /products?search=polo&status=active&sort=-created_at&cursor=…&limit=50
❌  const all = await listProducts(); all.filter(p => p.name.includes(q))
```

Convenciones: filtros opcionales y componibles (ausencia = sin ese filtro); búsqueda de texto en un param `search` donde el servidor decide las columnas; enums validados en el DTO. **Excepción acotada:** transformaciones puramente visuales (resaltar, agrupar lo ya traído) pueden ser client-side; *qué registros se muestran* siempre lo decide el backend.

---

## 8. Formato de respuesta

- **Timestamps**: ISO 8601 UTC (`"2026-09-01T14:30:00Z"`). Nunca epoch numérico ni formatos locales. (Ver `fechas-timezones.md`.)
- **Dinero**: enteros en la unidad menor (`priceCents: 8420`) o string con precisión (`"84.20"`). **Nunca float.**
- **IDs**: siempre strings, aunque internamente sean numéricos (JS pierde precisión con enteros grandes).
- **camelCase** en el JSON, aunque la DB use snake_case.

---

## 9. Evolución de la API y cambios rompedores

Una API es una pila de acuerdos (transporte, formato, campos, semántica, autorización). Cada consumidor tiene su propio calendario de despliegue: **no puedes obligarlos a actualizarse contigo.** Coordinar despliegues no escala.

**Principio de robustez (Postel):** sé conservador en lo que envías y liberal en lo que aceptas.

### Cambios seguros (aditivos)

- Aceptar un **superconjunto** de lo que se aceptaba (campos opcionales nuevos).
- Devolver un **superconjunto** de lo que se devolvía (campos nuevos en la respuesta).
- Exigir un **subconjunto** de lo que se exigía.
- Relajar una restricción.

### Cambios rompedores

- Quitar o renombrar un campo o endpoint.
- Añadir un campo **obligatorio** a la petición.
- Cambiar el tipo, formato o significado de un campo.
- Endurecer una validación que antes aceptaba el valor (la **implementación en producción es la especificación de facto**: si aceptabas un valor, no puedes rechazarlo sin romper).
- Exigir mayor nivel de autorización.
- Cambiar un código de estado que los clientes manejan.

### Cuando hay que romper

1. Prefiere un camino **aditivo**: campo nuevo junto al viejo, el viejo marcado como obsoleto.
2. Si no hay alternativa, **versiona** (prefiere la versión en la URL: `/v2/...`, simple de enrutar, cachear y filtrar en logs) y sube todas las rutas del recurso a la vez.
3. **Soporta la versión vieja y la nueva en paralelo** durante un plazo anunciado; prueba llamadas mezcladas sobre las mismas entidades.
4. Internamente, resuelve las versiones en el controller: convierte objeto viejo ↔ actual en la entrada y salida, y reutiliza la lógica.

### Consumidores defensivos

- Al **recibir**, acepta cualquier combinación de campos nuevos y define qué hacer ante los que faltan; no asumas el formato.
- Al **llamar** a otros servicios, trata la respuesta como datos hasta validarla; no la mapees ciegamente a objetos de dominio.
- Publica la especificación (OpenAPI) y prueba por **contratos**: el consumidor valida que arma bien la petición (lado request) y que sabe manejar cualquier respuesta permitida (lado response), sin invocar al proveedor. (Ver `testing.md` §9.)

---

## Prohibido

- Verbos en la URL (`/createOrder`).
- `200 OK` con error en el body.
- `throw new Error(...)` genérico en vez de excepción tipada con código.
- Colecciones sin límite de paginación (salvo catálogos acotados documentados).
- Filtrado de listas en el cliente.
- Confiar en headers del cliente para autorización.
- Tokens/PII en query params.
- Dinero como float; IDs como número.
- `202` cuando el trabajo ya terminó; `409` para input inválido.
- Cambios rompedores sin camino aditivo ni versión, o quitar la versión vieja sin plazo.

---

## Checklist al diseñar/limpiar un endpoint

- [ ] ¿El verbo HTTP es semánticamente correcto?
- [ ] ¿El código de estado es correcto (`201` create, `204` delete sin body, `200` update, `202` solo async real)?
- [ ] ¿Los errores son excepciones tipadas con `{ error: { code, message } }`?
- [ ] ¿Las colecciones paginan o tienen límite máximo?
- [ ] ¿Los filtros son server-side (query params → SQL)?
- [ ] ¿El tenant/org se valida contra el token, no contra el path/header?
- [ ] ¿Ningún token o PII viaja en query params?
- [ ] ¿Las acciones de dominio usan `POST` a sub-recurso?
- [ ] ¿Timestamps en ISO UTC, dinero sin float, IDs como string, JSON en camelCase?
- [ ] ¿El cambio es aditivo? Si rompe: ¿hay versión, convivencia y plazo?

---

## Cuándo aplicar

- **Siempre / hoy (nivel 1):** verbos y códigos correctos, error tipado con `code`, paginación y límites, filtrado server-side, tenant validado contra el token, formato de respuesta, y la regla de "no endurecer lo que ya aceptabas" (basta con que haya un solo cliente propio en producción: el navegador de un usuario tiene una versión vieja cacheada mientras despliegas).
- **Al crecer (nivel 2):** mantener los cambios aditivos de forma deliberada y desplegar backend antes que cliente; `Idempotency-Key` en operaciones críticas.
- **Con varios servicios o equipos (nivel 3):** versión en la URL con convivencia de versiones y plazo, especificación OpenAPI publicada, contract tests por lado (request/response) y política de deprecación comunicada a los consumidores.
