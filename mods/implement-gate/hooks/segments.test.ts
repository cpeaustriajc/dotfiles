import { expect, test } from 'claude-code/testing'
import { segments, targets } from './register'

// A seeded generator (mulberry32): a failure prints the seed.
const SEED = Date.now() % 2 ** 31
function rng(seed: number) {
  let a = seed
  return () => {
    a = (a + 0x6d2b79f5) | 0
    let t = Math.imul(a ^ (a >>> 15), 1 | a)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}
const one = <T>(r: () => number, xs: readonly T[]) => xs[Math.floor(r() * xs.length)] as T
const WORDS = ['gh', 'pr', 'merge', '7', 'git', 'push', 'origin', 'main', 'echo', 'hi', '--squash', 'x.txt']
const SEPS = [' && ', ' || ', '; ', ' | ', '\n']

test('property: a command joined by && || ; | or a line end splits into exactly its parts', async () => {
  const r = rng(SEED)
  for (let k = 0; k < 300; k++) {
    const parts = Array.from({ length: 1 + Math.floor(r() * 5) }, () => Array.from({ length: 1 + Math.floor(r() * 4) }, () => one(r, WORDS)).join(' '))
    const raw = parts.reduce((acc, p) => `${acc}${one(r, SEPS)}${p}`)
    expect(segments(raw).map(s => s.trim()), `seed ${SEED} run ${k}: ${JSON.stringify(raw)}`).toEqual(parts)
  }
})

test('property: a backslash line break never splits a command', async () => {
  const r = rng(SEED + 1)
  for (let k = 0; k < 300; k++) {
    const words = Array.from({ length: 2 + Math.floor(r() * 5) }, () => one(r, WORDS))
    const raw = words.join(' \\\n  ')
    expect(segments(raw).length, `seed ${SEED + 1} run ${k}`).toBe(1)
  }
})

test('property: a branch is a push target as a whole word, never as part of a longer name', async () => {
  const r = rng(SEED + 2)
  const forms = (b: string) => [b, `HEAD:${b}`, `+refs/heads/${b}`, `"${b}"`, `'${b}'`, `refs/heads/${b}`, `x:${b}`]
  for (let k = 0; k < 300; k++) {
    const b = one(r, ['main', 'master', 'trunk', 'release/1.2'])
    const lead = ` origin ${one(r, ['', '-u ', '--force-with-lease '])}`
    expect(targets(`${lead}${one(r, forms(b))}`, b), `seed ${SEED + 2} ${b}`).toBe(true)
    expect(targets(`${lead}${b}-fix`, b), `seed ${SEED + 2} ${b}-fix`).toBe(false)
    expect(targets(`${lead}feat/${b}`, b), `seed ${SEED + 2} feat/${b}`).toBe(false)
  }
})
