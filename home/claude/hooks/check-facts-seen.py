"""Lines from what Claude was told that share the most terms with a reply.
Used by check-facts.sh, which passes the transcript path as the argument and
the reply on stdin. Prints JSON with two lists of lines: owner (system prompt,
built-in tool descriptions, skill listing, instruction files) and others (MCP
server instructions, MCP tool descriptions, hook output)."""
import json, re, sys
path, reply = sys.argv[1], sys.stdin.read()
owner, others, shape = [], [], None
def leaves(v):
    if isinstance(v, str): yield v
    elif isinstance(v, dict):
        for x in v.values(): yield from leaves(x)
    elif isinstance(v, list):
        for x in v: yield from leaves(x)
def tools(ts):
    for t in ts or []:
        name = t.get("name") or ""
        (others if name.startswith("mcp__") else owner).append(f"tool {name}: {t.get('description', '')}")
# session_context and environment go to the judge whole, from check-facts.sh.
# A hook's block message quotes the claim it objected to, so it must not come
# back as a line that backs that claim.
skip = {"output_style", "file", "edited_text_file", "queued_command", "date",
        "session_context", "environment", "hook_blocking_error"}
for line in open(path):
    try: e = json.loads(line)
    except ValueError: continue
    if e.get("type") == "api-request-shape": shape = e.get("shape") or {}
    elif e.get("type") == "attachment":
        a = e.get("attachment") or {}
        kind = a.get("type") or ""
        if kind in skip: continue
        if kind == "prompt_snapshot":  # a copy of the prompt: its tools are split like the shape's
            owner.extend(leaves(a.get("systemPrompt")))
            tools(a.get("tools"))
        else:
            (others if kind.startswith(("mcp_", "hook_", "deferred_tools")) else owner).extend(leaves(a))
if shape:
    owner += [b.get("text", "") for b in shape.get("system", []) if isinstance(b, dict)]
    tools(shape.get("tools"))
stop = {"which", "would", "there", "their", "about", "these", "those", "because", "should", "before", "after"}
terms = {w.lower() for w in re.findall(r"`([^`]{3,60})`", reply)} | \
        {w.lower() for w in re.findall(r"[A-Za-z][\w.-]{5,}", reply)} - stop
def pick(texts, limit):
    chunks = {c.strip()[:300] for t in texts for c in re.split(r"\n+|(?<=[.!?])\s+", t) if len(c.strip()) > 20}
    scored = sorted(((sum(t in c.lower() for t in terms), c) for c in chunks), reverse=True)
    out, size = [], 0
    for s, c in scored:
        if s < 2 or size > limit: break
        out.append("- " + c); size += len(c)
    return "\n".join(out)
print(json.dumps({"owner": pick(owner, 6000), "others": pick(others, 2000)}))
