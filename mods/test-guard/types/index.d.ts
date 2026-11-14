export type Allowed = string[]
// HEAD and the losses already there at the start of the main loop's turn.
export type Turn = { root: string; sha: string; had: [string, string][] }
// tool.check's answer for one call: let through (the HEAD lines it loses, and whether a person's yes
// opens the path for the turn), or refused.
export type Call = { path: string; lost: string[]; opens?: true } | { deny: string }
// By path: each HEAD line a person approved losing, and how many times.
export type Approved = Record<string, Record<string, number>>
// The rules that run in one repository, picked by a small model at session start or typed by the user. `rigs`: the content rules only.
export type Mode = 'off' | 'rigs' | 'full'
// Kept in $.store under `profile:<remote or root>`, with the replay counts the choice was based on and who chose.
export type Profile = { mode: Mode; by?: 'model' | 'user'; at: string; commits: number; changes: number; full: number; rigs: number }

declare module 'claude-code' {
  interface PluginState {
    'test-guard': {
      allowed: Allowed
      turn: Turn | null
      noted: string[]
      calls: Record<string, Call>
      approved: Approved
      opened: string[]
    }
  }
}
