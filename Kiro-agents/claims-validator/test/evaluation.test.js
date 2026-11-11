// Reglas de evaluación y precedencia: REQ-010..016, REQ-030.

import assert from "node:assert/strict";
import { test } from "node:test";

import { Reason, Verdict } from "../src/constants.js";
import { makeEvaluator, validPayload } from "./support/fixtures.js";

test("valid claim passes all checks (REQ-016)", () => {
  const ev = makeEvaluator().evaluateRaw(validPayload());
  assert.equal(ev.verdict, Verdict.VALID);
  assert.deepEqual(ev.reasons, [Reason.ALL_CHECKS_PASSED]);
});

test("order not found (REQ-010)", () => {
  const p = validPayload();
  p.orderId = "ORD-DOES-NOT-EXIST";
  const ev = makeEvaluator().evaluateRaw(p);
  assert.equal(ev.verdict, Verdict.INVALID);
  assert.deepEqual(ev.reasons, [Reason.ORDER_NOT_FOUND]);
});

test("customer mismatch (REQ-011)", () => {
  const p = validPayload();
  p.customerId = "CUST-OTHER";
  const ev = makeEvaluator().evaluateRaw(p);
  assert.equal(ev.verdict, Verdict.INVALID);
  assert.deepEqual(ev.reasons, [Reason.CUSTOMER_MISMATCH]);
});

test("submitted before purchase (REQ-013)", () => {
  const p = validPayload();
  p.submittedAt = "2026-08-01T12:00:00Z";
  const ev = makeEvaluator().evaluateRaw(p);
  assert.equal(ev.verdict, Verdict.INVALID);
  assert.deepEqual(ev.reasons, [Reason.SUBMITTED_BEFORE_PURCHASE]);
});

test("claim window expired (REQ-012)", () => {
  const p = validPayload();
  p.submittedAt = "2026-10-05T12:00:00Z"; // compra 09-01 + 30d < 10-05
  const ev = makeEvaluator().evaluateRaw(p);
  assert.equal(ev.verdict, Verdict.INVALID);
  assert.deepEqual(ev.reasons, [Reason.CLAIM_WINDOW_EXPIRED]);
});

test("claim window boundary is valid (REQ-012)", () => {
  const p = validPayload();
  p.submittedAt = "2026-10-01T12:00:00Z"; // exacto +30d
  const ev = makeEvaluator().evaluateRaw(p);
  assert.equal(ev.verdict, Verdict.VALID);
});

test("refund exceeds order -> needs_review (REQ-014)", () => {
  const p = validPayload();
  p.resolution = "refund";
  p.amountRequestedCents = 15_000; // total es 10_000
  const ev = makeEvaluator().evaluateRaw(p);
  assert.equal(ev.verdict, Verdict.NEEDS_REVIEW);
  assert.ok(ev.reasons.includes(Reason.REFUND_EXCEEDS_ORDER));
});

test("refund within total is valid", () => {
  const p = validPayload();
  p.resolution = "refund";
  p.amountRequestedCents = 8_000;
  const ev = makeEvaluator().evaluateRaw(p);
  assert.equal(ev.verdict, Verdict.VALID);
});

test("category other -> needs_review (REQ-015)", () => {
  const p = validPayload();
  p.category = "other";
  const ev = makeEvaluator().evaluateRaw(p);
  assert.equal(ev.verdict, Verdict.NEEDS_REVIEW);
  assert.ok(ev.reasons.includes(Reason.CATEGORY_NEEDS_HUMAN));
});

test("precedence: invalid beats needs_review and cuts (REQ-030)", () => {
  const p = validPayload();
  p.category = "other"; // needs_review
  p.customerId = "CUST-OTHER"; // invalid
  const ev = makeEvaluator().evaluateRaw(p);
  assert.equal(ev.verdict, Verdict.INVALID);
  assert.deepEqual(ev.reasons, [Reason.CUSTOMER_MISMATCH]); // corta, no acumula
});

test("needs_review accumulates reasons (REQ-030 / concern)", () => {
  const p = validPayload();
  p.category = "other"; // needs_review 1
  p.resolution = "refund"; // needs_review 2
  p.amountRequestedCents = 99_999;
  const ev = makeEvaluator().evaluateRaw(p);
  assert.equal(ev.verdict, Verdict.NEEDS_REVIEW);
  assert.ok(ev.reasons.includes(Reason.REFUND_EXCEEDS_ORDER));
  assert.ok(ev.reasons.includes(Reason.CATEGORY_NEEDS_HUMAN));
});

test("evaluation output carries traceability (REQ-020/021)", () => {
  const ev = makeEvaluator().evaluateRaw(validPayload());
  const d = ev.toJSON();
  assert.equal(d.verdict, "valid");
  assert.ok(d.reasons.length > 0);
  assert.ok(d.decisionLog.length > 0);
  assert.ok(["note", "concern", "block"].includes(d.decisionLog[0].level));
});
