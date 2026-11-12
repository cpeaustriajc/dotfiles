export type Allowed = string[]
// HEAD and the losses already there at the start of the main loop's turn.
export type Turn = { root: string; sha: string; had: [string, string][] }

declare module 'claude-code' {
  interface PluginState {
    'test-guard': {
      allowed: Allowed
      turn: Turn | null
      noted: string[]
    }
  }
}
