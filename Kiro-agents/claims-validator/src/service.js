// Service: orquesta la evaluación. Aquí vive la decisión de negocio.
// Valida el input en el borde (schemas), busca la orden (repository) y aplica
// las reglas (rules) respetando la precedencia de REQ-030.

import { DecisionLevel, Reason, Verdict } from "./constants.js";
import { Evaluation } from "./models.js";
import { INVALID_RULES, NEEDS_REVIEW_RULES } from "./rules.js";
import { parseClaim } from "./schemas.js";

export class ClaimEvaluator {
  /** @param {import("./repository.js").OrderRepository} repository */
  constructor(repository) {
    this._repository = repository;
  }

  /** Punto de entrada desde el borde: valida y evalúa. */
  evaluateRaw(raw) {
    const claim = parseClaim(raw); // lanza ClaimValidationError si falla (REQ-002)
    return this.evaluate(claim);
  }

  /** @param {import("./models.js").Claim} claim */
  evaluate(claim) {
    const evaluation = new Evaluation(claim.claimId, Verdict.VALID);

    // REQ-010: la orden debe existir. Sin orden, invalid y corte.
    const order = this._repository.get(claim.orderId);
    if (order === undefined) {
      evaluation.verdict = Verdict.INVALID;
      evaluation.reasons.push(Reason.ORDER_NOT_FOUND);
      evaluation.addDecision(
        DecisionLevel.BLOCK,
        `Order ${claim.orderId} not found in catalog`,
      );
      return evaluation;
    }

    // REQ-030: reglas INVALID cortan en la primera que aplica.
    for (const rule of INVALID_RULES) {
      const r = rule(claim, order);
      if (r !== null) {
        evaluation.verdict = r.verdict;
        evaluation.reasons.push(r.reason);
        evaluation.addDecision(r.decision.level, r.decision.message);
        return evaluation;
      }
    }

    // REQ-014..015: reglas NEEDS_REVIEW no cortan; se acumulan ([concern]).
    for (const rule of NEEDS_REVIEW_RULES) {
      const r = rule(claim, order);
      if (r !== null) {
        evaluation.verdict = Verdict.NEEDS_REVIEW;
        evaluation.reasons.push(r.reason);
        evaluation.addDecision(r.decision.level, r.decision.message);
      }
    }

    // REQ-016: si nada se disparó, el reclamo es válido.
    if (evaluation.verdict === Verdict.VALID) {
      evaluation.reasons.push(Reason.ALL_CHECKS_PASSED);
      evaluation.addDecision(DecisionLevel.NOTE, "All checks passed");
    }

    return evaluation;
  }
}
