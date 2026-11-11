# Requisitos — Listar reclamos ingresados

> Formato EARS. Continúa la numeración del MVP (REQ-040+).
> Esta feature agrega **persistencia de los reclamos ingresados** y su **listado**.
> Hasta ahora el sistema evaluaba e imprimía, pero no guardaba el reclamo.

## Persistencia del reclamo ingresado

- **REQ-040** — WHEN se evalúa un reclamo válido en su contrato de borde,
  THE SYSTEM SHALL registrar el reclamo ingresado junto con el `verdict` y los
  `reasons` resultantes de su evaluación.
- **REQ-041** — IF el reclamo no supera la validación de borde (REQ-002),
  THEN THE SYSTEM SHALL NO registrarlo como reclamo ingresado.
- **REQ-042** — THE SYSTEM SHALL conservar el orden de ingreso de los reclamos
  (el primero ingresado es el primero listado).

## Listado

- **REQ-043** — WHEN se solicita el listado, THE SYSTEM SHALL devolver, por cada
  reclamo ingresado, al menos: `claimId`, `orderId`, `customerId`, `category`,
  `resolution`, `submittedAt` (ISO-8601 UTC), `verdict` y `reasons`.
- **REQ-044** — IF no hay reclamos ingresados, THEN THE SYSTEM SHALL devolver una
  lista vacía (no un error).
