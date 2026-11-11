// Catálogo de órdenes: solo lee/escribe datos (REQ-010).
// Implementación en memoria para el demo ([note] en 03-design.md). La interfaz
// permite sustituirla por una DB sin tocar el service.

import { createOrder } from "./models.js";

export class OrderRepository {
  /** @param {Map<string, import("./models.js").Order>} [orders] */
  constructor(orders) {
    this._orders = orders ?? new Map();
  }

  /** @param {string} orderId @returns {import("./models.js").Order | undefined} */
  get(orderId) {
    return this._orders.get(orderId);
  }

  /** @param {import("./models.js").Order} order */
  add(order) {
    this._orders.set(order.orderId, order);
  }
}

/** Repository con órdenes de ejemplo para la demo del CLI. */
export function seededRepository() {
  const repo = new OrderRepository();
  repo.add(
    createOrder({
      orderId: "ORD-1001",
      customerId: "CUST-1",
      purchasedAt: new Date("2026-09-20T10:00:00Z"),
      totalAmountCents: 12_000, // $120.00
      items: [{ sku: "SKU-A", quantity: 1, unitPriceCents: 12_000 }],
    }),
  );
  repo.add(
    createOrder({
      orderId: "ORD-1002",
      customerId: "CUST-2",
      purchasedAt: new Date("2026-01-05T10:00:00Z"),
      totalAmountCents: 5_000, // $50.00, compra antigua
      items: [{ sku: "SKU-B", quantity: 2, unitPriceCents: 2_500 }],
    }),
  );
  return repo;
}
