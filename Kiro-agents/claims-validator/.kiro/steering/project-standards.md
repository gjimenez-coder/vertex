---
inclusion: always
---

# Claims Validator — Estándares del proyecto

> Steering siempre activo. Fija el vocabulario, las capas y las reglas no negociables.
> Alineado con las prácticas de Firehorse (spec → build, trazabilidad, revisión local)
> y con los principios de dominio/backend del repo.

## Vocabulario de dominio (fuente de verdad)

- **Claim (reclamo)**: solicitud de un cliente pidiendo una resolución sobre una compra.
- **Resolution (resolución)**: lo que el cliente pide (reembolso, reemplazo, reparación).
- **Verdict (veredicto)**: salida del sistema — `valid`, `invalid` o `needs_review`.
- **Reason (motivo)**: código estable que justifica el veredicto.
- **Decision log**: notas/concerns/blocks que el evaluador deja al decidir (trazabilidad).

## Stack

- **Node.js** (>=20), **ESM** (`"type": "module"`, imports con extensión `.js`).
- Tests con el runner nativo **`node:test`** + `node:assert/strict`. Sin dependencias externas.

## Capas (la lógica de negocio vive en el Service)

```
entrypoint (cli.js)   →  valida y delega, no decide
schemas.js (DTO)      →  valida el input en el borde, tipa la salida
service.js            →  TODA la decisión de negocio ocurre aquí
rules.js              →  reglas puras y testeables, sin I/O
repository.js         →  solo lee/escribe datos (en memoria para este demo)
constants.js          →  enums y umbrales de dominio (NO en schemas)
errors.js             →  errores tipados del dominio
```

## Reglas no negociables

- Dinero: **entero en centavos**, nunca float. Usa `Number.isInteger`.
- Fechas: instantes en **UTC** (`Date` desde ISO-8601 con zona). No formatear para humanos en el backend.
- Nada hardcodeado: umbrales y ventanas de tiempo viven en `constants.js`/config, no en el service.
- Validación en el borde: todo input entra por un schema explícito antes de ejecutar lógica.
- Errores tipados: el dominio levanta clases de error propias, no strings sueltos.
- Enums de dominio: objetos congelados con `Object.freeze`, no literales sueltos.
- Trazabilidad: cada veredicto incluye el o los `reason` y el decision log que lo sustenta.
- Toda regla de validación mapea a un requisito (REQ-xxx) y queda cubierta por un test.

## Organización de specs (convención Kiro)

- El dominio transversal vive en `docs/01-domain.md` (no pertenece a un solo spec).
- Cada feature es **su propia carpeta** en `.kiro/specs/<feature>/`, en `kebab-case`,
  con tres archivos de nombre fijo:
  - `requirements.md` — requisitos EARS (REQ-xxx).
  - `design.md` — diseño + decisiones note/concern/block + constraints.
  - `tasks.md` — plan de implementación trazable a los REQ.
- El MVP vive en `.kiro/specs/claims-mvp/`. Un feature = un spec = (idealmente) un MR.

## Flujo de trabajo (del material de Firehorse)

1. **Spec primero**: dominio → requisitos (EARS) → diseño, con decisiones marcadas
   como `note` / `concern` / `block`.
2. **Build después**: implementa exactamente lo que dice el spec, sin inventar alcance.
3. **Gate local antes de entregar**: tests en verde localmente antes de "merge".
