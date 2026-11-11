// Validación de borde: convierte input crudo (objeto) en un Claim tipado.
// Implementa REQ-001, REQ-002, REQ-003 y los constraints C-1, C-2.
// No ejecuta lógica de evaluación; solo valida el contrato de entrada.

import { CLAIM_CATEGORIES, RESOLUTIONS, Resolution } from "./constants.js";
import { ClaimValidationError } from "./errors.js";
import { createClaim } from "./models.js";

const REQUIRED_FIELDS = [
  "claimId",
  "orderId",
  "customerId",
  "category",
  "resolution",
  "submittedAt",
];

const ISO_WITH_TZ = /(?:Z|[+-]\d{2}:\d{2})$/;

/** Acepta ISO-8601 con zona; devuelve Date UTC o null si inválido (C-2). */
function parseUtc(value) {
  if (typeof value !== "string" || !ISO_WITH_TZ.test(value)) return null;
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? null : d;
}

function isPlainInteger(value) {
  // Rechaza booleans (que en JS no son typeof number) y no-enteros.
  return typeof value === "number" && Number.isInteger(value);
}

/**
 * Valida `raw` y devuelve un Claim, o lanza ClaimValidationError.
 * Acumula todas las violaciones para reportarlas juntas (REQ-002).
 * @param {unknown} raw
 */
export function parseClaim(raw) {
  if (raw === null || typeof raw !== "object" || Array.isArray(raw)) {
    throw new ClaimValidationError(["payload must be an object"]);
  }

  /** @type {string[]} */
  const errors = [];

  // REQ-001: campos obligatorios presentes.
  for (const field of REQUIRED_FIELDS) {
    const v = raw[field];
    if (v === undefined || v === null || v === "") {
      errors.push(`'${field}' is required`);
    }
  }

  // Enums tipados.
  if (raw.category !== undefined && raw.category !== null && raw.category !== "") {
    if (!CLAIM_CATEGORIES.includes(raw.category)) {
      errors.push(`'category' must be one of ${JSON.stringify(CLAIM_CATEGORIES)}`);
    }
  }

  let resolution = null;
  if (
    raw.resolution !== undefined &&
    raw.resolution !== null &&
    raw.resolution !== ""
  ) {
    if (RESOLUTIONS.includes(raw.resolution)) {
      resolution = raw.resolution;
    } else {
      errors.push(`'resolution' must be one of ${JSON.stringify(RESOLUTIONS)}`);
    }
  }

  // Instante UTC válido.
  let submittedAt = null;
  if (
    raw.submittedAt !== undefined &&
    raw.submittedAt !== null &&
    raw.submittedAt !== ""
  ) {
    submittedAt = parseUtc(raw.submittedAt);
    if (submittedAt === null) {
      errors.push("'submittedAt' must be an ISO-8601 datetime with timezone");
    }
  }

  // REQ-003: refund exige amountRequestedCents entero > 0.
  const amount = raw.amountRequestedCents;
  if (resolution === Resolution.REFUND) {
    if (!isPlainInteger(amount)) {
      errors.push("'amountRequestedCents' must be an integer for refunds");
    } else if (amount <= 0) {
      errors.push("'amountRequestedCents' must be greater than zero");
    }
  } else if (amount !== undefined && amount !== null) {
    // Si viene en otros casos, debe ser entero válido (C-1).
    if (!isPlainInteger(amount)) {
      errors.push("'amountRequestedCents' must be an integer");
    }
  }

  if (errors.length > 0) {
    throw new ClaimValidationError(errors);
  }

  return createClaim({
    claimId: raw.claimId,
    orderId: raw.orderId,
    customerId: raw.customerId,
    category: raw.category,
    resolution,
    submittedAt,
    amountRequestedCents: isPlainInteger(amount) ? amount : null,
    description: typeof raw.description === "string" ? raw.description : "",
  });
}
