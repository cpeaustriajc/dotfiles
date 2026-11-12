# Models: getting weights, and the environments

## When a hub is slow, measure before waiting

A download that "is running" can be stalled. Check the cache size twice, seconds apart, and compare
hosts with `curl -w "%{speed_download}"` on a hub file range and on
`https://speed.cloudflare.com/__down?bytes=25000000`.

October 2026 launch: Hugging Face about 200 KB/s per connection, Cloudflare 24 MB/s; a 4.5 GB model
would have taken six hours. Parallel ranges helped about 5x; the fix was another source.

**ModelScope** (`modelscope.cn`) hosts Qwen's official weights and mirrors popular models under the
same repo name (`facebook/musicgen-medium`, `AI-ModelScope/...`); it served 10-15 MB/s.
`scripts/modelscope_download.py <repo> <dest> [skip,files]` downloads in parallel 64 MB ranges with
retries and size checks. Load the local folder (`load_model("<dest>")`) with `HF_HUB_OFFLINE=1`.
Check a mirror's file list first; it may hold several weight formats.

## Environments

One environment per heavy stack:
- `tts-venv`: `uv venv --python 3.12 tts-venv && uv pip install --python tts-venv/bin/python --prerelease=allow mlx-audio soundfile`
- `music-venv`: `transformers torch soundfile numpy`, plus `openai-whisper` for word timings.

State each download's size before starting, run long ones in the background with progress in the
log, and remove models and environments only after the person approves the output.
