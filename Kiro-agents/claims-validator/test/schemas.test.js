// Validación de borde: REQ-001, REQ-002, REQ-003, C-2.

import assert from "node:assert/strict";
import { test } from "node:test";

import { ClaimCategory, Resolution } from "../src/constants.js";
import { ClaimValidationError } from "../src/errors.js";
import { parseClaim } from "../src/schemas.js";
import { validPayload } from "./support/fixtures.js";

test("parses a valid payload", () => {
  const claim = parseClaim(validPayload());
  assert.equal(claim.claimId, "CLM-1");
  assert.equal(claim.category, ClaimCategory.DAMAGED);
  assert.equal(claim.resolution, Resolution.REPLACEMENT);
  assert.ok(claim.submittedAt instanceof Date); // normalizado a Date UTC (C-2)
});

test("missing required fields raises and accumulates (REQ-002)", () => {
  const p = validPayload();
  delete p.orderId;
  delete p.customerId;
  assert.throws(
    () => parseClaim(p),
    (err) => {
      assert.ok(err instanceof ClaimValidationError);
      assert.ok(err.errors.some((e) => e.includes("orderId")));
      assert.ok(err.errors.some((e) => e.includes("customerId")));
      return true;
    },
  );
});

test("invalid enum raises", () => {
  const p = validPayload();
  p.category = "exploded";
  assert.throws(() => parseClaim(p), ClaimValidationError);
});

test("refund requires amount (REQ-003)", () => {
  const p = validPayload();
  p.resolution = "refund";
  assert.throws(
    () => parseClaim(p),
    (err) => {
      assert.ok(err.errors.some((e) => e.includes("amountRequestedCents")));
      return true;
    },
  );
});

test("refund rejects zero amount", () => {
  const p = validPayload();
  p.resolution = "refund";
  p.amountRequestedCents = 0;
  assert.throws(() => parseClaim(p), ClaimValidationError);
});

test("naive datetime rejected (C-2)", () => {
  const p = validPayload();
  p.submittedAt = "2026-09-10T12:00:00"; // sin tz
  assert.throws(
    () => parseClaim(p),
    (err) => {
      assert.ok(err.errors.some((e) => e.includes("submittedAt")));
      return true;
    },
  );
});

test("rejects boolean as amount (not a plain integer)", () => {
  const p = validPayload();
  p.amountRequestedCents = true;
  assert.throws(() => parseClaim(p), ClaimValidationError);
});
