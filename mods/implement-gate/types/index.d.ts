export type Level = 'commit' | 'pr' | 'ready' | 'merged'

declare module 'claude-code' {
  interface PluginState {
    'implement-gate': {
      level: Level | null
      blocks: number
      head: string | null
    }
  }
}
