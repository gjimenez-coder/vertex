# Requisitos — Validador de reclamos retail

> Formato EARS. Cada REQ es trazable al diseño y a un test.
> Palabras clave: WHEN (evento), IF (condición), THE SYSTEM SHALL (obligación).

## Entrada y validación de borde

- **REQ-001** — THE SYSTEM SHALL aceptar un reclamo únicamente si trae `claimId`,
  `orderId`, `customerId`, `category`, `resolution` y `submittedAt`.
- **REQ-002** — IF algún campo obligatorio falta o tiene un tipo inválido,
  THEN THE SYSTEM SHALL rechazar la entrada con un error de validación tipado,
  sin ejecutar lógica de evaluación.
- **REQ-003** — IF `resolution` es `refund`, THEN THE SYSTEM SHALL requerir
  `amountRequestedCents` como entero mayor que cero.

## Reglas de evaluación

- **REQ-010** — WHEN se evalúa un reclamo, IF la `orderId` no existe en el catálogo,
  THEN THE SYSTEM SHALL devolver veredicto `invalid` con motivo `ORDER_NOT_FOUND`.
- **REQ-011** — WHEN se evalúa un reclamo, IF la `customerId` del reclamo no coincide
  con la de la orden, THEN THE SYSTEM SHALL devolver `invalid` con motivo
  `CUSTOMER_MISMATCH`.
- **REQ-012** — WHEN se evalúa un reclamo, IF `submittedAt` ocurre después de la
  ventana de reclamo contada desde `purchasedAt`, THEN THE SYSTEM SHALL devolver
  `invalid` con motivo `CLAIM_WINDOW_EXPIRED`.
- **REQ-013** — WHEN se evalúa un reclamo, IF `submittedAt` es anterior a
  `purchasedAt`, THEN THE SYSTEM SHALL devolver `invalid` con motivo
  `SUBMITTED_BEFORE_PURCHASE`.
- **REQ-014** — WHEN la `resolution` es `refund`, IF `amountRequestedCents` es mayor
  que `totalAmountCents` de la orden, THEN THE SYSTEM SHALL devolver `needs_review`
  con motivo `REFUND_EXCEEDS_ORDER`.
- **REQ-015** — WHEN la `category` es `other`, THE SYSTEM SHALL devolver
  `needs_review` con motivo `CATEGORY_NEEDS_HUMAN`.
- **REQ-016** — WHEN un reclamo pasa todas las reglas anteriores sin disparar
  `invalid` ni `needs_review`, THE SYSTEM SHALL devolver `valid` con motivo
  `ALL_CHECKS_PASSED`.

## Salida y trazabilidad

- **REQ-020** — THE SYSTEM SHALL incluir en cada evaluación el `verdict`, la lista de
  `reasons` y el `decisionLog`.
- **REQ-021** — THE SYSTEM SHALL registrar en el `decisionLog` cada decisión relevante
  clasificada como `note`, `concern` o `block`.
- **REQ-022** — THE SYSTEM SHALL expresar todo monto en centavos (entero) y todo
  instante en UTC.

## Precedencia

- **REQ-030** — IF más de una regla aplica, THEN THE SYSTEM SHALL priorizar en este
  orden: `invalid` (REQ-010..013) sobre `needs_review` (REQ-014..015) sobre `valid`.
  Un `invalid` detiene la evaluación de reglas posteriores.
