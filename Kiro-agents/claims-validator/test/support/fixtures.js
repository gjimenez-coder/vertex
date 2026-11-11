// Fixtures compartidos para los tests.

import { createOrder } from "../../src/models.js";
import { OrderRepository } from "../../src/repository.js";
import { ClaimEvaluator } from "../../src/service.js";

export function makeOrder() {
  return createOrder({
    orderId: "ORD-1001",
    customerId: "CUST-1",
    purchasedAt: new Date("2026-09-01T12:00:00Z"),
    totalAmountCents: 10_000,
    items: [{ sku: "SKU-A", quantity: 1, unitPriceCents: 10_000 }],
  });
}

export function makeEvaluator() {
  const order = makeOrder();
  const repo = new OrderRepository(new Map([[order.orderId, order]]));
  return new ClaimEvaluator(repo);
}

/** Reclamo que pasa todas las reglas contra la orden del fixture. */
export function validPayload() {
  return {
    claimId: "CLM-1",
    orderId: "ORD-1001",
    customerId: "CUST-1",
    category: "damaged",
    resolution: "replacement",
    submittedAt: "2026-09-10T12:00:00Z",
  };
}
