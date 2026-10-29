# Changelog

## 0.4.1

Removed the `$schema` key from `.claude-plugin/plugin.json`. The Claude Agent SDK does not recognize it and showed a warning each time the skill loaded (same fix as blader/humanizer #307). No change to the patterns.

## 0.4.0

Three rounds of fixes measured on the 30-text evaluation, then checked on 20 new texts (`tests/eval/README.md`). On the new texts, facts kept rose from 89.3% to 95.1% and added facts fell from 4 to 0. The AI-judge win rate stayed within noise (92% to 98%).

- New rule in Step 2: cut wrappers, not meaning. Words for degree, certainty, conditions, cause and purpose, the writer's own verdict or advice, and who is speaking are content, and keep the strength the source gave them (`SKILL.md`).
- A closing summary may be cut only after its claims are moved into the body (`SKILL.md`).
- The draft check now compares the source and the draft one sentence at a time, including the opening line and any closing promise (`SKILL.md`).
- A text with only a few tells gets a light touch: casual posts keep their particles, English words, calls to action, and loose formatting (`SKILL.md`).
- The evaluation has a held-out set (`tests/eval/holdout/`) and a stricter fact check.

## 0.3.0

Fixes from the first evaluation on 30 Thai texts, where v0.2.0 reached a 93% AI-judge win rate and kept 97.6% of facts.

- When a draft offers several versions and the user did not pick one, rewrite only the first and say how many were left out (`SKILL.md`, TH-26). Before, the rewrite kept every version.
- Template pronouns such as "ผม/ดิฉัน" now follow the particle rule: never choose the writer's gender (`SKILL.md`, TH-22).
- The draft check now asks whether a claim became more or less certain. Hedges such as "อาจ" and "น่าจะ" stay, and promises stay promises (`SKILL.md`, TH-27). TH-27 now cuts only the AI's notes about its own knowledge.

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
