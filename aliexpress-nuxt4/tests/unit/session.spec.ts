import { describe, expect, it } from 'vitest'
import { extractTokens, removeTokens } from '../../server/utils/session-payload'

describe('BFF session payload handling', () => {
  it('extracts a valid token pair from the upstream envelope', () => {
    expect(extractTokens({ success: true, data: { access: 'access-token', refresh: 'refresh-token' } }))
      .toEqual({ access: 'access-token', refresh: 'refresh-token' })
  })

  it('does not expose token fields in the browser payload', () => {
    expect(removeTokens({ success: true, data: { access: 'access-token', refresh: 'refresh-token', profile: { id: '1' } } }))
      .toEqual({ success: true, data: { profile: { id: '1' } } })
  })

  it('rejects malformed upstream token payloads', () => {
    expect(extractTokens({ success: true, data: { access: 42 } })).toBeNull()
  })
})
