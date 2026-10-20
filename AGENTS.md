# Guide for agents

This repo is an Agent Skill written in Markdown. There is no build step.

## Files

- `SKILL.md` is the entry point. It holds the shared workflow and tells the agent which reference file to read. Keep it short: it is read on every use.
- `references/patterns-th.md` holds the Thai patterns, written in Thai. IDs are `TH-n`.
- `references/patterns-en.md` holds the English patterns. IDs are `EN-n`.
- `references/mixed-th-en.md` holds rules for mixed text. IDs are `MX-n`.
- `examples/` holds worked examples used for manual testing.
- `tests/eval/` holds a repeatable evaluation on 30 Thai texts. After a change to the skill, run it as `tests/eval/README.md` describes and add a row to its results table.
- `scripts/validate-package.py` checks versions, descriptions, pattern numbering, README tables, pattern ID references, and file sizes.

## Rules for changes

- Number patterns in each file from 1 without gaps. If you add, remove, or renumber a pattern, update the README tables and every ID reference in `SKILL.md`, the other pattern files, and `examples/`.
- Add a new pattern only when no existing one already covers it. Prefer extending an existing pattern's watch list.
- Every Thai pattern needs a real-looking before and after. The after must not add facts the before lacks; if an example needs a detail to read well, say in a note that the detail must come from the source.
- Keep the same version in `SKILL.md` (`metadata.version`), the first `CHANGELOG.md` heading, `.claude-plugin/plugin.json`, and `.cursor-plugin/plugin.json`.
- Every manifest description is the first sentence of the `SKILL.md` description.
- Size limits are in characters, because Thai has no spaces between words.
- Keep install and usage instructions neutral across agents.
- Run `python3 scripts/validate-package.py` before committing.

## Writing style

Plain language in both languages: lead with the point, use common words, keep sentences short, and use one term for one thing. In Thai, separate sentences with a space, not with English punctuation.
