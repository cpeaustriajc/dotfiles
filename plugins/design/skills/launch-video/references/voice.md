# Voice: a local narrator that sounds like a person

## Pick the model by evidence, not memory

Check a current arena (Artificial Analysis TTS leaderboard, TTS Arena) and each licence: many top
open-weights models are non-commercial, which rules them out for an ad. On Apple Silicon, `mlx-audio`
(MIT) runs most on the GPU.

October 2026 launch results:

| Model | Result |
|---|---|
| Kokoro-82M | Fast, flat. Read "lives" as *laives*, "Renav" as *ruh-NAV*. Phonemiser looked for espeak data in a hard-coded CI path; needed Homebrew `espeak-ng`. Pitch-shifting with ffmpeg still sounded synthetic. |
| Qwen3-TTS CustomVoice (presets) | Expressive, but Chinese-native speakers sounded like dubbed television to an English listener. |
| Qwen3-TTS VoiceDesign, one call per line | Natural, but each call designs a new voice: lines sounded like different people. |
| Qwen3-TTS Base, cloning one clip | One voice, flat: Base takes no delivery instructions. |
| **Qwen3-TTS VoiceDesign, whole script in one call** | **One voice, natural, directed per paragraph. Used.** |

## The one-take method

1. Describe the voice specifically: accent and what to avoid, age, timbre, register. Example:
   > A native General American English speaker, a woman in her late twenties from California. Neutral
   > standard American accent; absolutely no foreign, Asian or British accent. Warm, slightly husky
   > mid-range, natural and unpolished. A real person talking to a friend. Not a news anchor, not a
   > commercial announcer, not a dubbed drama voice. Natural breaths, small pauses, relaxed rhythm.
2. Direct each paragraph inside the same instruction ("Paragraph 1: puzzled, mild upward inflection
   ... Paragraph 4: light rising questions, pitch lifting most on 'Lisbon'"). Blank lines between
   script lines make the take pause.
3. Three seeds with `scripts/onetake_narrate.py`, joined by `scripts/audition.py`; the person picks by
   ear. Any text change regenerates the whole take: keep the liked take in a named file and generate
   the edit on that seed and two neighbours.
4. Cut the pick into lines with `scripts/split_take.py`: Whisper word timestamps (`openai-whisper`,
   `small.en`; weights come from OpenAI's server, not a hub) find the gaps. Whisper may drop a word
   like "Euros?": find that onset from the audio level. Output: one WAV per line plus a timing file
   (duration, word onsets) that drives the cues.
5. Retime the film to the voice: place each line at its frame, check no overlap, move cues to word
   onsets.

## Writing for the ear

- Punctuation is direction: `?` rises, `…` pauses, `?!` lifts with surprise; the same items with `!`
  read as stressed. Adjust one word at a time.
- Stretch a vowel in the direction, not the spelling: "riiight" was read *reeet*; "All right there!"
  with "draw out 'right', the long 'eye' vowel as in 'bright'" worked.
- Respell names for the voice only, never on screen. Check phonemes first:
  `espeak-ng -q --ipa -v en-us "Ree-nav"` gives `ɹˈiːnˈæv`. Record the pronunciation in the
  project's memory.
- A line the model rambles past (22 s for a 5 s line) is a failed generation: regenerate on another
  seed; do not keep the spelling that caused it.
