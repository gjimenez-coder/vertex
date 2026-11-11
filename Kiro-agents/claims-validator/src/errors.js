// Errores tipados del dominio (REQ-002, C-4).
// El borde (schemas) levanta estos errores; el service no arma mensajes a mano.

export class ClaimsValidatorError extends Error {
  constructor(message) {
    super(message);
    this.name = "ClaimsValidatorError";
  }
}

/**
 * El input del reclamo no cumple el contrato del borde (REQ-001..003).
 * Agrupa una o más violaciones de campo para reportarlas juntas.
 */
export class ClaimValidationError extends ClaimsValidatorError {
  /** @param {string[]} errors */
  constructor(errors) {
    super(errors.join("; "));
    this.name = "ClaimValidationError";
    this.errors = errors;
  }
}
