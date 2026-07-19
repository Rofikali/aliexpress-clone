import { describe, expect, it } from "vitest"

import { handleApiError, normalizeResponse } from "../../app/utils/api/base"
import { createIdempotencyKey, createRequestId } from "../../app/shared/api/identifiers"

describe("API response normalization", () => {
  it("preserves the public response contract", () => {
    expect(normalizeResponse({ success: 1, code: 200, message: "OK", data: { id: 1 } })).toEqual({
      success: true,
      code: 200,
      message: "OK",
      data: { id: 1 },
    })
  })

  it("normalizes an HTTP error without leaking response data", () => {
    expect(handleApiError({ response: { status: 403 }, message: "Forbidden" })).toEqual({
      success: false,
      code: 403,
      message: "Forbidden",
      data: null,
    })
  })

  it("uses the backend's safe error message when provided", () => {
    expect(handleApiError({
      response: { status: 409, data: { message: "Insufficient inventory" } },
      message: "Request failed",
    })).toEqual({
      success: false,
      code: 409,
      message: "Insufficient inventory",
      data: null,
    })
  })

  it("creates UUIDs for correlation and checkout idempotency", () => {
    expect(createRequestId()).toMatch(/^[0-9a-f-]{36}$/)
    expect(createIdempotencyKey()).toMatch(/^[0-9a-f-]{36}$/)
  })
})
