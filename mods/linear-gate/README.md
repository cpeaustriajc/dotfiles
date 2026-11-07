# linear-gate

A mod (a plugin that adds a hook to Claude Code) that blocks Linear writes outside your shift. On shift, your permission mode decides, and the mod asks you only before a delete, retire or cancel.

## Why

A Linear write is visible to your whole team, and Linear can post it to Slack. After your shift, one write can notify your team at night.

On shift, a dialog for every write costs you many clicks. Auto mode can decide most writes. linear-gate asks you only before writes that remove or cancel work, in Claude Code's own permission dialog.

## Install

```
/plugin marketplace add cpeaustriajc/dotfiles
/plugin install linear-gate@dotfiles
```

To see that it is on, run `claude plugin list` and look for `linear-gate`. The install steps in the root README include this mod.

## Example

1. At 20:35, after your 18:00 shift end, Claude calls the Linear tool `save_issue`.
2. The mod denies the call. No dialog opens.
3. Claude reads the reason and puts the draft in the chat.

Claude reads:

```
linear-gate: off shift (09:00-18:00); a Linear write notifies the team's Slack. Do not retry: draft it in the chat for the next shift.
```

At 10:00, the same call goes to your permission mode. A call that moves ACME-77 to Canceled opens the permission dialog with the reason "linear-gate: Cancel issue ACME-77. Everyone on the team sees this." You allow or deny it. Auto mode cannot allow it for you.

## What it does

| Event | Decision |
|---|---|
| Claude or a subagent calls a Linear write tool off shift | Deny it, also in a headless session. |
| Claude calls a Linear write tool on shift | Leave it to your permission mode. |
| Claude calls a delete, retire or cancel on shift | Ask you in the permission dialog. |
| Claude calls a Linear read tool | Let it pass. |
| Auto mode would allow the asked write | Ask you anyway. Only you, the host's callback or a `PermissionRequest` hook can allow it. |
| A host program answers the session's permission asks | The host decides. |
| Nobody can be asked, as in a plain `claude -p` run | Deny the call. Claude reads the reason. |

The reason names the action, such as "Create issue" or "Merge PR", and the issue, PR or document. For a document edit, it names the document by its title.

A delete, a retire or a cancel adds "Everyone on the team sees this."

The mod treats a tool as a write if its name is in the list in `hooks/register.tsx`. A tool on the `linear-server` server is also a write if its name starts with a write verb such as `save_`, `delete_` or `update_`.

## Settings

| Option | Default | Meaning |
|---|---|---|
| `shiftStart` | `09:00` | The local time your shift starts, 24-hour. |
| `shiftEnd` | `18:00` | The local time your shift ends. A start after the end crosses midnight. |
| `timeZone` | empty | An IANA zone such as `Asia/Manila`. Empty uses the zone of your machine. |
| `onShift` | `drastic` | `host`: your permission mode decides every write. `drastic`: ask before a delete, retire or cancel. `ask`: ask before every write. |

An hour that is not `HH:MM` makes both hours fall back to 09:00 and 18:00. Run `claude plugin configure linear-gate@dotfiles` to set them on your machine.

To turn the mod off, run `claude plugin disable linear-gate@dotfiles`.

## Limits

- A write tool from another server passes if its name is not in the list.
- A write tool with a new name on `linear-server` is gated only if it starts with a write verb.
- The dialog shows one line. It does not show the fields, the text or a diff of the change.
- If the document title lookup fails, the reason shows the short document id.

## More

- [hooks/register.tsx](hooks/register.tsx): the hook source.
- [hooks/register.test.ts](hooks/register.test.ts): the tests for the asks and their reasons.
- [hooks/shift.test.ts](hooks/shift.test.ts): the tests for the shift hours and the `onShift` option.
- [marketplace.json](../../.claude-plugin/marketplace.json): the manifest, in this mod's entry.
- [.claude-plugin/plugin.json](.claude-plugin/plugin.json): the options and their defaults (`userConfig`).
