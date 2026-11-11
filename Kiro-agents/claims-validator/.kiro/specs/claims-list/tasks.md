# Tareas — Listar reclamos ingresados

> Plan de implementación del spec `claims-list`. Cada tarea referencia los
> requisitos que satisface.

- [ ] 1. Repositorio de reclamos (_REQ-042, REQ-044, C-11_)
  - `repository.js`: `ClaimRepository` en memoria (Map, orden de inserción).
  - `save(entry)` guarda/actualiza por `claimId`; `list()` devuelve array (vacío si no hay).

- [ ] 2. Registro en el service (_REQ-040, REQ-041, C-10_)
  - `service.js`: `ClaimEvaluator` acepta un `ClaimRepository` opcional y registra
    el reclamo + veredicto tras evaluar. No registra si el borde falla.
  - `listClaims()` expone la proyección estable del listado (_REQ-043, C-12_).

- [ ] 3. Comando CLI --list (_REQ-043, REQ-044_)
  - `cli.js`: modo `--list` imprime los reclamos ingresados como JSON.

- [ ] 4. Gate local (verificación)
  - `test/claims-list.test.js`: registra tras evaluar, no registra en borde inválido,
    preserva orden, upsert por claimId, lista vacía.
  - `npm test` en verde (incluye los tests del MVP).
