// Reglas de evaluación puras: reciben Claim + Order, no hacen I/O (C-5).
// Cada función implementa un requisito y devuelve un RuleResult o null (no aplica).
// Separar reglas del service permite testear cada REQ aislado.

import {
  CLAIM_WINDOW_DAYS,
  ClaimCategory,
  DecisionLevel,
  MS_PER_DAY,
  Reason,
  Resolution,
  Verdict,
} from "./constants.js";

/**
 * @typedef {Object} RuleResult
 * @property {string} verdict
 * @property {string} reason
 * @property {{ level: string, message: string }} decision
 */

/** @param {string} verdict @param {string} reason @param {string} level @param {string} message @returns {RuleResult} */
function result(verdict, reason, level, message) {
  return { verdict, reason, decision: { level, message } };
}

// ── Reglas que producen INVALID (REQ-010..013) ───────────────────────

/** REQ-011: la orden debe pertenecer al cliente del reclamo. */
export function checkCustomerMatch(claim, order) {
  if (claim.customerId !== order.customerId) {
    return result(
      Verdict.INVALID,
      Reason.CUSTOMER_MISMATCH,
      DecisionLevel.BLOCK,
      `Claim customer ${claim.customerId} does not own order ${order.orderId}`,
    );
  }
  return null;
}

/** REQ-013: no se puede reclamar antes de comprar. */
export function checkNotBeforePurchase(claim, order) {
  if (claim.submittedAt.getTime() < order.purchasedAt.getTime()) {
    return result(
      Verdict.INVALID,
      Reason.SUBMITTED_BEFORE_PURCHASE,
      DecisionLevel.BLOCK,
      "Claim submitted before the purchase instant",
    );
  }
  return null;
}

/** REQ-012: el reclamo debe caer dentro de la ventana desde la compra. */
export function checkClaimWindow(claim, order) {
  const deadline = order.purchasedAt.getTime() + CLAIM_WINDOW_DAYS * MS_PER_DAY;
  if (claim.submittedAt.getTime() > deadline) {
    return result(
      Verdict.INVALID,
      Reason.CLAIM_WINDOW_EXPIRED,
      DecisionLevel.NOTE,
      `Claim window of ${CLAIM_WINDOW_DAYS} days expired ` +
        `(deadline ${new Date(deadline).toISOString()})`,
    );
  }
  return null;
}

// ── Reglas que producen NEEDS_REVIEW (REQ-014..015) ──────────────────

/** REQ-014: un reembolso mayor al total de la orden escala a humano. */
export function checkRefundAmount(claim, order) {
  if (
    claim.resolution === Resolution.REFUND &&
    claim.amountRequestedCents !== null &&
    claim.amountRequestedCents > order.totalAmountCents
  ) {
    return result(
      Verdict.NEEDS_REVIEW,
      Reason.REFUND_EXCEEDS_ORDER,
      DecisionLevel.CONCERN,
      `Refund requested (${claim.amountRequestedCents}) exceeds ` +
        `order total (${order.totalAmountCents})`,
    );
  }
  return null;
}

/** REQ-015: la categoría 'other' siempre necesita revisión humana. */
export function checkCategoryOther(claim) {
  if (claim.category === ClaimCategory.OTHER) {
    return result(
      Verdict.NEEDS_REVIEW,
      Reason.CATEGORY_NEEDS_HUMAN,
      DecisionLevel.CONCERN,
      "Category 'other' cannot be auto-decided",
    );
  }
  return null;
}

// Orden de precedencia (REQ-030): invalid primero, luego needs_review.
export const INVALID_RULES = [
  checkCustomerMatch,
  checkNotBeforePurchase,
  checkClaimWindow,
];

export const NEEDS_REVIEW_RULES = [checkRefundAmount, checkCategoryOther];
