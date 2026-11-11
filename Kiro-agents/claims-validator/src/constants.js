// Enums de dominio y umbrales. Única fuente de constantes (REQ-022, C-3).
// No viven en schemas ni como literales dentro de rules.

/** Tipifica el problema reclamado. */
export const ClaimCategory = Object.freeze({
  DAMAGED: "damaged",
  NOT_DELIVERED: "not_delivered",
  WRONG_ITEM: "wrong_item",
  LATE: "late",
  OTHER: "other",
});

/** Lo que el cliente pide. */
export const Resolution = Object.freeze({
  REFUND: "refund",
  REPLACEMENT: "replacement",
  REPAIR: "repair",
});

/** Salida del evaluador. */
export const Verdict = Object.freeze({
  VALID: "valid",
  INVALID: "invalid",
  NEEDS_REVIEW: "needs_review",
});

/** Severidad de una entrada del decision log. */
export const DecisionLevel = Object.freeze({
  NOTE: "note",
  CONCERN: "concern",
  BLOCK: "block",
});

/** Códigos estables que justifican un veredicto (REQ-010..016). */
export const Reason = Object.freeze({
  ORDER_NOT_FOUND: "ORDER_NOT_FOUND",
  CUSTOMER_MISMATCH: "CUSTOMER_MISMATCH",
  CLAIM_WINDOW_EXPIRED: "CLAIM_WINDOW_EXPIRED",
  SUBMITTED_BEFORE_PURCHASE: "SUBMITTED_BEFORE_PURCHASE",
  REFUND_EXCEEDS_ORDER: "REFUND_EXCEEDS_ORDER",
  CATEGORY_NEEDS_HUMAN: "CATEGORY_NEEDS_HUMAN",
  ALL_CHECKS_PASSED: "ALL_CHECKS_PASSED",
});

// Conjuntos de valores válidos, para la validación de borde.
export const CLAIM_CATEGORIES = Object.freeze(Object.values(ClaimCategory));
export const RESOLUTIONS = Object.freeze(Object.values(Resolution));

// ── Umbrales de dominio ──────────────────────────────────────────────
// Ventana de reclamo global (REQ-012). Punto de extensión: podría variar por
// categoría de producto (ver [concern] en 03-design.md).
export const CLAIM_WINDOW_DAYS = 30;
export const MS_PER_DAY = 24 * 60 * 60 * 1000;
