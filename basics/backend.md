---
inclusion: manual
---

# Backend — Principios Reutilizables

> Alcance: capa de servidor (lógica de negocio, persistencia, procesos). Independiente de framework. Complementa `arquitectura-software.md` (capas, módulos, transacciones), `apis.md` (contrato HTTP), `modelado-dominio.md` (datos) y `seguridad.md`.

---

## 1. La lógica de negocio vive en el Service

- Toda decisión de negocio ocurre en la capa **Service**, no en el controller ni en el repository.
- El controller valida y delega; el repository solo lee/escribe datos. (Capas y dirección de dependencias: `arquitectura-software.md` §1.)

---

## 2. Agrupa lo atómico

- Agrupa en una sola transacción todo lo que debe confirmarse o revertirse junto.
- No dejes escrituras relacionadas fuera de la transacción que las coordina.
- **No metas efectos externos dentro de la transacción** (email, HTTP a terceros, cobros): si la transacción aborta, el efecto ya ocurrió. Persiste un evento (outbox, §3) y ejecuta el efecto después.

> Dónde se abre la transacción y cómo se propaga: `arquitectura-software.md` §2.

---

## 3. Eventos diferidos (outbox)

- Para efectos secundarios diferidos (notificaciones, side effects cross-módulo), usa **outbox**: la escritura principal y el evento se persisten en la **misma transacción**, y un handler los procesa después.
- El procesamiento es **at-least-once**: el mismo evento puede entregarse más de una vez. Todo handler debe ser **idempotente**.
- Un evento sin handler registrado queda en estado fallido para revisión; nunca se descarta en silencio.

### Receptor de eventos

Quien consume eventos (otro módulo, otro servicio) debe:

- **Deduplicar** por el `eventId` del evento.
- **Ignorar** eventos más viejos que el último aplicado a la misma entidad (los reintentos pueden llegar fuera de orden).
- Responder `2xx` también ante duplicados, para que el emisor deje de reintentar.
- **Tolerar campos nuevos** que no conoce, y no fallar por un campo opcional ausente.

### Versionado del payload

Un evento persistido puede procesarse con una versión del código distinta de la que lo creó (rolling deploy, reintentos tardíos).

- Incluye un campo `version` en el payload.
- El handler acepta la versión actual **y la anterior** durante la ventana de despliegue.
- Cambios de payload siguen las reglas de compatibilidad de `apis.md` §9.

```
✅  { eventId, type: 'payment.status_changed', version: 2, occurredAt, data }
❌  handler que asume el shape más reciente y falla con eventos viejos en cola
```

---

## 4. Procesos automáticos y autoría

- Cuando un proceso automático (job, handler, migración, seed) ejecuta una acción con campo de autoría, ese campo debe ser un actor explícito (`'system'`), **nunca `null`/`undefined`**. Preserva la trazabilidad.

```
✅  actor: actorId ?? 'system'
❌  actor: undefined
```

---

## 5. Migraciones de base de datos

Separa **generar** de **aplicar**:

- **Generar** la migración es una decisión **humana y revisada**. No se genera ni se ejecuta como efecto colateral de un cambio de código (ni por un agente automático).
- **Aplicar** una migración ya revisada puede ir en el pipeline de despliegue, siempre compatible hacia atrás (expand/contract, ver `cicd.md` §4).
- Flujo al cambiar el esquema: modifica la definición → actualiza tipos/interfaces/DTOs afectados → **informa** que debe generarse la migración.
- No ejecutes seeds automáticamente; solo si se solicita.

```
✅  "Agregué el campo `newField` al schema. Genera y revisa la migración cuando estés listo."
❌  (ejecutar generate/migrate/push automáticamente tras editar el schema)
```

---

## 6. Configuración y secretos

- **Nunca hardcodees** TTLs, límites, URLs ni secretos: vienen de configuración validada al arrancar.
- Flujo para un valor nuevo: declararlo en el esquema de entorno con default → exponerlo con un getter tipado → consumirlo desde ahí.
- Los secretos nunca viven en el repo: cómo se gestionan, en `seguridad.md` §13.

```
❌  const expiresAt = Date.now() + 15 * 60 * 1000
✅  const expiresAt = Date.now() + config.checkoutTtlSeconds * 1000
```

> Esta es la única definición de esta regla; los demás documentos la enlazan.

---

## 7. Validación en el borde

- Valida todo input que entra al servidor contra un **esquema explícito** antes de ejecutar lógica. No confíes en que el cliente ya validó.
- Rechaza temprano con errores tipados (ver `apis.md` §3 y `manejo-errores.md`).
- Campos que el cliente no debe controlar (precios, roles, tenant) **nunca** vienen del body: se resuelven en el servidor (ver `seguridad.md` §8).

---

## 8. Fechas en el backend

Instantes en UTC, días calendario como `YYYY-MM-DD`, y la TZ solo como lógica de negocio. Ver `fechas-timezones.md`.

---

## 9. Concurrencia sobre saldos y estado

Varias peticiones tocan la misma fila al mismo tiempo. Un patrón leer → decidir → escribir pierde actualizaciones si no se protege.

- **Prefiere la operación atómica**: `UPDATE saldo SET qty = qty - $1 WHERE id = $2 AND qty >= $1`, y revisa cuántas filas afectó.
- Si debes leer antes de decidir, **bloquea la fila** (`SELECT … FOR UPDATE`) dentro de la transacción. Con varias filas, bloquéalas siempre en el **mismo orden** para evitar deadlocks.
- Para condiciones que dependen de **varias filas** (por ejemplo "debe quedar al menos una persona de guardia"), bloquea todas las filas de las que depende la decisión o usa una restricción en la base de datos.
- Los saldos se derivan de un **ledger append-only** (ver `modelado-dominio.md` §6): nunca se edita el saldo "a mano".
- Reintenta una transacción solo ante errores **transitorios** (deadlock, fallo de serialización), con límite y backoff. Un error de dominio no mejora al reintentarse.
- Haz las operaciones con efectos **idempotentes** (ID determinístico o clave de idempotencia) para que un reintento no duplique.

```
✅  UPDATE stock SET on_hand = on_hand - $1 WHERE sku = $2 AND on_hand >= $1
❌  const s = await getStock(sku); if (s.onHand >= q) await setStock(sku, s.onHand - q)
```

---

## 10. Flujos entre servicios

Cuando una operación toca más de un servicio no hay transacción distribuida (ver `arquitectura-software.md` §9). Se coordina con transacciones locales:

- Modela el flujo como pasos con **estado explícito**. Un estado `*_PENDING` actúa como **bloqueo semántico**: avisa a otros procesos que el registro está en curso.
- Distingue los pasos: **compensables** (se pueden deshacer), un **pivote** (el punto sin retorno) y **reintentables** (garantizados tras el pivote).
- Cada paso compensable define su **compensación** explícita (cancelar, liberar, revertir).
- Usa orquestación (un coordinador con máquina de estados) para flujos de más de dos pasos; la coreografía por eventos solo para flujos simples.

---

## Prohibido

- Lógica de negocio en controllers o repositories.
- Efectos externos dentro de una transacción de base de datos.
- Efectos diferidos no idempotentes; handlers que asumen entrega única u ordenada.
- Payloads de eventos sin `version` consumidos por código de otra versión.
- Autoría `null`/`undefined` en procesos automáticos.
- Generar o ejecutar migraciones o seeds como efecto colateral de editar código.
- TTLs, URLs o secretos hardcodeados.
- Leer → decidir → escribir un saldo sin operación atómica ni bloqueo.
- Reintentar errores de dominio.

---

## Checklist

- [ ] ¿La lógica de negocio está en el Service?
- [ ] ¿Las escrituras relacionadas van en una sola transacción, sin efectos externos dentro?
- [ ] ¿Los efectos diferidos usan outbox y los handlers son idempotentes?
- [ ] ¿El receptor deduplica por `eventId`, ignora eventos viejos y responde `2xx` ante duplicados?
- [ ] ¿Los payloads de eventos llevan `version` y el handler tolera la anterior?
- [ ] ¿Los procesos automáticos registran actor explícito?
- [ ] ¿Los cambios de schema informan la migración en vez de generarla o ejecutarla solos?
- [ ] ¿No hay TTLs/URLs/secretos hardcodeados?
- [ ] ¿Todo input se valida contra un esquema en el servidor?
- [ ] ¿Los saldos se modifican con operación atómica o bloqueo en orden fijo?
- [ ] ¿Los flujos entre servicios tienen estados explícitos y compensaciones definidas?

---

## Cuándo aplicar

- **Siempre / hoy (nivel 1):** lógica en el Service, validación en el borde, config sin hardcodear, autoría `'system'`, separar generar de aplicar migraciones, operaciones atómicas o `FOR UPDATE` sobre saldos (aunque haya una sola instancia: dos requests concurrentes ya bastan), outbox idempotente para efectos diferidos.
- **Al crecer (nivel 2):** `version` en el payload de eventos y compatibilidad con la versión anterior (aparece con despliegues rolling y varias instancias); reintentos transaccionales con backoff.
- **Con varios servicios o equipos (nivel 3):** receptor de eventos con deduplicación y orden entre servicios, orquestación de flujos con compensaciones explícitas, estados `*_PENDING` como bloqueo semántico.
