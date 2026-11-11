// Factories de las entidades del dominio (ver docs/01-domain.md).
// Dinero en centavos (int), instantes en UTC (Date). Objetos congelados para
// evitar mutación accidental durante la evaluación.

/** @typedef {{ sku: string, quantity: number, unitPriceCents: number }} OrderItem */

/**
 * @typedef {Object} Order
 * @property {string} orderId
 * @property {string} customerId
 * @property {Date}   purchasedAt         instante UTC
 * @property {number} totalAmountCents    entero, centavos
 * @property {OrderItem[]} items
 */

/**
 * @typedef {Object} Claim
 * @property {string} claimId
 * @property {string} orderId
 * @property {string} customerId
 * @property {string} category
 * @property {string} resolution
 * @property {Date}   submittedAt         instante UTC
 * @property {number|null} amountRequestedCents
 * @property {string} description
 */

/**
 * @typedef {Object} DecisionEntry
 * @property {string} level    note | concern | block (REQ-021)
 * @property {string} message
 */

export function createOrder({
  orderId,
  customerId,
  purchasedAt,
  totalAmountCents,
  items = [],
}) {
  return Object.freeze({
    orderId,
    customerId,
    purchasedAt,
    totalAmountCents,
    items: Object.freeze([...items]),
  });
}

export function createClaim({
  claimId,
  orderId,
  customerId,
  category,
  resolution,
  submittedAt,
  amountRequestedCents = null,
  description = "",
}) {
  return Object.freeze({
    claimId,
    orderId,
    customerId,
    category,
    resolution,
    submittedAt,
    amountRequestedCents,
    description,
  });
}

/** Resultado de evaluar un reclamo (REQ-020). Mutable: se arma durante la evaluación. */
export class Evaluation {
  /** @param {string} claimId @param {string} verdict */
  constructor(claimId, verdict) {
    this.claimId = claimId;
    this.verdict = verdict;
    /** @type {string[]} */
    this.reasons = [];
    /** @type {DecisionEntry[]} */
    this.decisionLog = [];
  }

  /** @param {string} level @param {string} message */
  addDecision(level, message) {
    this.decisionLog.push({ level, message });
  }

  toJSON() {
    return {
      claimId: this.claimId,
      verdict: this.verdict,
      reasons: this.reasons,
      decisionLog: this.decisionLog,
    };
  }
}
