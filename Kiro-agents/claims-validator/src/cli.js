#!/usr/bin/env node
// Entrypoint CLI: recibe un reclamo en JSON, delega al service, imprime el veredicto.
// El entrypoint valida/parsea y delega; no toma decisiones de negocio.
//
// Uso:
//   node src/cli.js '<json>'          # reclamo inline
//   echo '<json>' | node src/cli.js   # reclamo por stdin
//   node src/cli.js --demo            # corre ejemplos sembrados

import { ClaimValidationError } from "./errors.js";
import { seededRepository } from "./repository.js";
import { ClaimEvaluator } from "./service.js";

const DEMO_CLAIMS = [
  {
    claimId: "CLM-1",
    orderId: "ORD-1001",
    customerId: "CUST-1",
    category: "damaged",
    resolution: "replacement",
    submittedAt: "2026-09-25T10:00:00Z",
  },
  {
    claimId: "CLM-2",
    orderId: "ORD-1002",
    customerId: "CUST-2",
    category: "late",
    resolution: "refund",
    amountRequestedCents: 9_000,
    submittedAt: "2026-09-25T10:00:00Z",
  },
  {
    claimId: "CLM-3",
    orderId: "ORD-9999",
    customerId: "CUST-1",
    category: "wrong_item",
    resolution: "repair",
    submittedAt: "2026-09-25T10:00:00Z",
  },
];

function evaluateAndPrint(evaluator, raw) {
  try {
    const evaluation = evaluator.evaluateRaw(raw);
    console.log(JSON.stringify(evaluation.toJSON(), null, 2));
  } catch (err) {
    if (err instanceof ClaimValidationError) {
      console.log(
        JSON.stringify(
          { error: "validation_failed", details: err.errors },
          null,
          2,
        ),
      );
      return;
    }
    throw err;
  }
}

function readStdin() {
  return new Promise((resolve) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => (data += chunk));
    process.stdin.on("end", () => resolve(data));
  });
}

export async function main(argv = process.argv.slice(2)) {
  const evaluator = new ClaimEvaluator(seededRepository());

  if (argv[0] === "--demo") {
    for (const raw of DEMO_CLAIMS) {
      evaluateAndPrint(evaluator, raw);
      console.log("-".repeat(40));
    }
    return 0;
  }

  const payload = argv.length > 0 ? argv[0] : await readStdin();

  let raw;
  try {
    raw = JSON.parse(payload);
  } catch (err) {
    console.log(
      JSON.stringify({ error: "invalid_json", details: err.message }, null, 2),
    );
    return 1;
  }

  evaluateAndPrint(evaluator, raw);
  return 0;
}

// Ejecuta solo si se invoca directamente (no al importarse en tests).
if (import.meta.url === `file://${process.argv[1]}`) {
  main().then((code) => process.exit(code));
}
