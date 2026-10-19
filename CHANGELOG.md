# Changelog

## 0.2.0

Tuned the Thai patterns against real output from ChatGPT, Claude, and Gemini (`tests/samples/`).

- New section in `SKILL.md`: keep placeholders such as `[ชื่อแบรนด์]` unfilled, and after the rewrite list the specs, dates, causes, and comparisons the writer should check. Real drafts invented many of these.
- Extended watch lists in TH-1, TH-2, TH-3, TH-12, TH-13, TH-16, TH-17, TH-18, TH-21, TH-22, TH-25, TH-26, and TH-27 with phrases seen in the samples, such as "ใครว่า...", "ไว้มีโอกาสต้องกลับมาอีกแน่นอน", "แรงขับเคลื่อนหลัก", "ครับ/ค่ะ" written as a pair, and suggestion chips copied from the chat app.
- TH-3 and TH-18 now say to keep a real claim inside a stock phrase. TH-26 now says to move useful advice from cut notes into the check list, and to ask which version to keep when a draft offers several.
- MX-1 covers English words dropped into Thai grammar more often than a team would say them.
- New worked example from real output: `examples/th-real-fb-post.md`.
- Pasted text now returns only the final version and the check list by default. The draft and the tell list appear only when the user asks.
- TH-25 keeps a list whose lines each carry their own fact (specs, prices, order channels) instead of merging it into a paragraph.

## 0.1.0

First release.

- `SKILL.md` with a shared rewrite workflow for Thai, English, and mixed text. The agent reads only the pattern file for the language it finds.
- 28 Thai patterns (`references/patterns-th.md`), including translated-sounding Thai, paragraph-opening connectors, register mixing, and particles.
- 23 English patterns (`references/patterns-en.md`), adapted from blader/humanizer 3.1.0.
- Rules for text that mixes Thai and English (`references/mixed-th-en.md`).
- Worked examples in `examples/` and a package validator that measures Thai files in characters, since Thai has no spaces between words.
