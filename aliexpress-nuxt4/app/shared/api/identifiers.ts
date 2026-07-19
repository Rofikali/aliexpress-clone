export function createRequestId(): string {
  return globalThis.crypto.randomUUID()
}

export function createIdempotencyKey(): string {
  return globalThis.crypto.randomUUID()
}
