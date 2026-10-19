# Changelog

## 0.1.0

First release.

- `SKILL.md` with a shared rewrite workflow for Thai, English, and mixed text. The agent reads only the pattern file for the language it finds.
- 28 Thai patterns (`references/patterns-th.md`), including translated-sounding Thai, paragraph-opening connectors, register mixing, and particles.
- 23 English patterns (`references/patterns-en.md`), adapted from blader/humanizer 3.1.0.
- Rules for text that mixes Thai and English (`references/mixed-th-en.md`).
- Worked examples in `examples/` and a package validator that measures Thai files in characters, since Thai has no spaces between words.
