# Diseño — Listar reclamos ingresados

> Cómo se implementa el spec `claims-list`. Reutiliza las capas del MVP:
> el service decide y persiste, el repository solo guarda/lee datos, el CLI delega.

## Mapa requisito → componente

| Requisito     | Dónde vive |
|---------------|------------|
| REQ-040..041  | `service.js` (registra tras evaluar; no registra si el borde falla) |
| REQ-042       | `repository.js` (`ClaimRepository`, orden de inserción) |
| REQ-043       | `service.js` + `models.js` (proyección del reclamo ingresado) |
| REQ-044       | `repository.js` (lista vacía por defecto) |

## Flujo

1. El CLI recibe el reclamo (inline/stdin) y delega en `ClaimEvaluator.evaluateRaw`.
2. El service valida en el borde (schemas). Si falla → error tipado y **no** persiste
   (REQ-041).
3. Si valida, evalúa (reglas MVP) y **registra** el reclamo + su veredicto en el
   `ClaimRepository` (REQ-040).
4. El modo `--list` del CLI pide `evaluator.listClaims()` y lo imprime como JSON.

## Decisiones de diseño

- **[note] ClaimRepository en memoria.** Mismo criterio que el catálogo de órdenes:
  un `Map` preserva el orden de inserción (REQ-042) y la interfaz permite cambiarlo
  por una DB sin tocar el service. En el CLI de un solo proceso, el listado vive
  mientras corre el proceso.
- **[note] El service es dueño de la persistencia.** El registro ocurre en
  `service.js` (capa de decisión), después de evaluar, para que un reclamo rechazado
  en el borde nunca se registre (REQ-041). El repository no decide, solo guarda.
- **[concern] Idempotencia por `claimId`.** El MVP no define qué pasa si llega dos
  veces el mismo `claimId`. Decisión para esta feature: se registra la última
  evaluación bajo ese `claimId` (upsert), evitando duplicados en el listado.
  Revisar si el negocio exige historial completo por reclamo.
- **[note] Proyección estable para el listado.** El listado no expone el objeto
  interno `Evaluation` completo; devuelve una proyección plana y estable (REQ-043)
  con el instante en ISO-8601 UTC (REQ-022 del MVP sigue vigente).

## Constraints para el build

- C-10: El registro ocurre en el service, nunca en el CLI ni en las reglas.
- C-11: El `ClaimRepository` preserva orden de inserción y no muta los reclamos ya
  guardados (objetos congelados, como en `models.js`).
- C-12: La proyección del listado serializa `submittedAt` como ISO-8601 UTC.
