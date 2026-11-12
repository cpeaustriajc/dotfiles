# Music: a local bed under the voice

MusicGen (`facebook/musicgen-medium`) through `transformers` on Apple MPS: about 30 s per
generation, ignores BPM and key (put the mood in the prompt). The loader needs `pytorch_model.bin`
(8 GB) plus config and tokenizer; `state_dict.bin` is not needed. Mirror: `models.md`.

1. Two or three candidates with `scripts/musicgen.py`: one matching the voice's tone (a quirky
   narrator: pizzicato, claps, marimba), one safer.
2. Loop the pick to the film's length and fade the ends:
   ```sh
   ffmpeg -i track.wav -i track.wav -filter_complex \
     "[0][1]acrossfade=d=2:c1=tri:c2=tri,atrim=0:36,afade=t=in:d=0.4,afade=t=out:st=33.5:d=2.5" bed.wav
   ```
3. Mix at `data-volume="0.2"` under a full-level voice; `ffmpeg -i out.mp4 -af volumedetect -vn -f null -`
   must show a max below 0 dB.
4. Say which track is in and offer the other; music is settled by ear.
