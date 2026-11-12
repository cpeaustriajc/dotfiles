# Worst-case catalog

Step 5 of `SKILL.md`. Source: Emil Kowalski's `break-ui` skill,
https://raw.githubusercontent.com/emilkowalski/skill/main/skills/break-ui/SKILL.md and
https://raw.githubusercontent.com/emilkowalski/skill/main/skills/break-ui/CATALOG.md. Take from
it: worst-case values per field type (text, numbers, collections, time, images, states,
viewport), chosen from the fields the flow shows.

House rules on top of it:

- Take each field's limit from the validation schema, the database column, the API type or the
  input's `maxLength`; write "unbounded" where none exists. A front-end limit that differs from the
  back-end limit is a finding.
- Name each value and the rule it attacks ("a 63-character label stays on one line"), not only a
  technique.
- Put the values in through the same seam as the demo data: fixture, mock, props or API stub.
  Never edit the markup to cause a break.
- Truncation is decided per field. Wrap what the user needs in full to identify an item. Cut at the
  end only where the start carries the meaning, and give a way to see the full value. Cut in the
  middle where items differ at the end (file names, paths, hashes). Never cut numbers, money,
  dates or anything the user compares. One rule for every field is a finding.
- Keep the worst-case fixture as a regression test unless told otherwise. The toggle stays
  dev-only.
