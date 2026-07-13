import { describe, expect, it } from "vitest"

import { handleApiError, normalizeResponse } from "../../app/utils/api/base"

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
})
