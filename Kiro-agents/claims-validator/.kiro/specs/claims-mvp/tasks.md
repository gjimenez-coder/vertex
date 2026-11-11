# Tareas — Validador de reclamos retail (MVP)

> Plan de implementación del spec `claims-mvp`. Cada tarea referencia los
> requisitos que satisface. Marcadas como completadas de forma retroactiva: el
> MVP ya está construido y verificado (gate local en verde).

- [x] 1. Capas base del dominio (_REQ-022_)
  - Enums de dominio y umbrales en `constants.js` (Object.freeze).
  - Errores tipados en `errors.js`.
  - Entidades `Order`, `Claim`, `Evaluation` en `models.js`.

- [x] 2. Validación de borde (_REQ-001, REQ-002, REQ-003_)
  - `schemas.js`: `parseClaim` valida campos obligatorios, enums, instante UTC
    (rechaza fechas sin zona) y monto de refund entero > 0.
  - Acumula todas las violaciones en un `ClaimValidationError`.

- [x] 3. Catálogo de órdenes (_REQ-010_)
  - `repository.js`: `OrderRepository` en memoria + `seededRepository`.

- [x] 4. Reglas de evaluación puras (_REQ-010..016_)
  - Reglas INVALID: orden inexistente, cliente no coincide, antes de la compra,
    fuera de ventana.
  - Reglas NEEDS_REVIEW: refund mayor al total, categoría `other`.

- [x] 5. Orquestación en el service (_REQ-020, REQ-021, REQ-030_)
  - `service.js`: `ClaimEvaluator` aplica precedencia invalid > needs_review >
    valid, con corte temprano en invalid y acumulación en needs_review.
  - Cada veredicto sale con `reasons` + `decisionLog`.

- [x] 6. Entrypoint CLI (_REQ-020_)
  - `cli.js`: modos `--demo`, inline y stdin. Valida y delega, no decide.

- [x] 7. Gate local (verificación)
  - Tests `node:test` por regla, precedencia y borde (`test/`).
  - `npm test` en verde; `node src/cli.js --demo` end-to-end.
