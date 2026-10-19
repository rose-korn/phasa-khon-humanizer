# Phasa Khon Humanizer (ภาษาคน)

[อ่านภาษาไทย](README.th.md)

Phasa Khon Humanizer rewrites AI-sounding **Thai** and **English** text so it reads like a person wrote it, without changing what it says. "พูดภาษาคน" (*phut phasa khon*, "speak human") is a Thai idiom for saying something plainly. It is an Agent Skill, so it works in Claude Code, Claude.ai, Codex, Cursor, and any other agent that supports skills.

**Before (Thai):**
> ในยุคปัจจุบันที่ร้านกาแฟเกิดขึ้นมากมาย ปฏิเสธไม่ได้ว่าการหาร้านที่ใช่นั้นไม่ใช่เรื่องง่าย ... ร้านนี้ไม่ใช่แค่ร้านกาแฟ แต่คือพื้นที่แห่งความสุขที่ตอบโจทย์ทุกไลฟ์สไตล์ ... นอกจากนี้ เมล็ดกาแฟของร้านยังถูกคัดสรรมาอย่างพิถีพิถันจากดอยสะเก็ด ... กล่าวโดยสรุป ... บอกเลยว่าห้ามพลาด!

**After:**
> ร้าน "บ้านไม้" เป็นร้านกาแฟเล็กๆ ที่แม่ริม เชียงใหม่ รอบร้านเป็นต้นไม้ นั่งทำงานหรือถ่ายรูปได้ เมล็ดกาแฟมาจากดอยสะเก็ด ลาเต้เย็นแก้วละ 65 บาท

The full example is in [examples/th-blog-review.md](examples/th-blog-review.md).

The goal is writing that people want to read. Getting past AI detectors is not a goal.

## What is different for Thai

Thai AI text has tells that English lists miss:

- **Translated Thai.** The Thai follows English grammar: "ถูกพัฒนาขึ้น" for a neutral passive, "มัน" for "it", "ทำการ/มีการ" before every verb, "เมื่อพูดถึง..." for "when it comes to".
- **Stock openers and closers.** "ในยุคปัจจุบัน...", "ปฏิเสธไม่ได้ว่า...", "กล่าวโดยสรุป", "บอกเลยว่าห้ามพลาด!"
- **Connectors by rule.** "นอกจากนี้", "อย่างไรก็ตาม", "ดังนั้น" at the start of every paragraph.
- **Particles and register.** ครับ/ค่ะ at the end of every sentence, "นะคะ" in a formal notice, formal and slang Thai in one paragraph.
- **Typography.** English punctuation and em dashes in Thai prose, and an English term in brackets after every Thai term.

Mixing English words into Thai is normal and is not treated as a tell. The skill keeps the writer's loanwords and their ครับ or ค่ะ.

## Installation

Once installed, the skill answers to `/phasa-khon-humanizer`.

### Claude Code

```text
/plugin marketplace add Pisitkorn-Bootchada/phasa-khon-humanizer
/plugin install phasa-khon-humanizer@phasa-khon-humanizer
```

### Codex, Cursor, Gemini CLI, and other agents

```bash
npx skills add Pisitkorn-Bootchada/phasa-khon-humanizer --global --agent '*'
```

Leave off `--global` to install it only in the current project.

### Claude.ai and Claude Desktop

Download this repository as a ZIP (**Code → Download ZIP**) and upload it as a skill in Settings.

## Usage

```
/phasa-khon-humanizer

[paste your text]
```

Or ask in plain language, in either language:

```
ช่วยเขียนข้อความนี้ใหม่ให้อ่านเหมือนคนเขียน: [ข้อความ]
Humanize the prose in docs/announcement.md
Does this caption sound like AI? [caption]
```

To match your voice, add two or three paragraphs of your own writing before the text. The skill follows your sentence length, particles, loanwords, and punctuation.

## How it works

`SKILL.md` holds the shared workflow: mark the tells, draft, check that no fact was added or lost, and write the final version. The agent then reads only the pattern file for the language it finds, which keeps the prompt short:

| File | Contents |
|------|----------|
| [`references/patterns-th.md`](references/patterns-th.md) | Thai patterns, written in Thai |
| [`references/patterns-en.md`](references/patterns-en.md) | English patterns |
| [`references/mixed-th-en.md`](references/mixed-th-en.md) | Rules for text that mixes Thai and English |

## The patterns

### Thai

| ID | Pattern | In English |
|----|---------|------------|
| TH-1 | ไม่ใช่แค่... แต่ยัง... | Not just X but Y |
| TH-2 | เปิดเรื่องสำเร็จรูป | Stock openers |
| TH-3 | ปิดท้ายสำเร็จรูปและประโยคปิดสั้นๆ | Stock closers |
| TH-4 | เกริ่นก่อนเข้าเรื่อง | Run-up before the point |
| TH-5 | คำคมกลวง | Sayings that sound deep |
| TH-6 | "ถูก" และ "ได้รับการ" ในความหมายกลางหรือดี | Neutral passives with ถูก |
| TH-7 | คำนาม "การ/ความ" ซ้อนกัน และ "ทำการ/มีการ/ดำเนินการ" | Stacked nouns and empty verbs |
| TH-8 | "มัน" และ "คุณ" ตามภาษาอังกฤษ | "It" and "you" copied from English |
| TH-9 | "ซึ่ง" และ "ที่" ต่อกันเป็นสาย | Chains of relative clauses |
| TH-10 | สำนวนแปลตรงตัว | Literal translations |
| TH-11 | คำเชื่อมขึ้นต้นทุกย่อหน้า | A connector opening every paragraph |
| TH-12 | สามอย่างเสมอ และ "ไม่ว่าจะเป็น A, B หรือ C" | Forced triads |
| TH-13 | คำขยายติดท้ายกริยา | "Effectively" after every verb |
| TH-14 | ขึ้นต้นประโยคซ้ำ | Repeated openings |
| TH-15 | ขีดยาวและเครื่องหมายวรรคตอนแบบอังกฤษ | Dashes and English punctuation |
| TH-16 | คำฮิตของ AI ภาษาไทย | Overused AI words |
| TH-17 | ทำให้เรื่องธรรมดาดูยิ่งใหญ่ | Inflated significance |
| TH-18 | ภาษาโฆษณา | Sales language |
| TH-19 | อ้างผู้เชี่ยวชาญลอยๆ | Unnamed experts |
| TH-20 | หลีกเลี่ยง "เป็น" และ "มี" | Avoiding "is" and "has" |
| TH-21 | ปนระดับภาษา | Mixed register |
| TH-22 | คำลงท้ายตามสูตร | Particles by rule |
| TH-23 | น้ำเสียงตื่นเต้นแบบแปล | Translated excitement |
| TH-24 | วงเล็บภาษาอังกฤษตามหลังทุกศัพท์ | English in brackets after every term |
| TH-25 | ตัวหนา อีโมจิ และหัวข้อตามสูตร | Bold, emojis, and headings by rule |
| TH-26 | ประโยคแชตบอต | Chatbot residue |
| TH-27 | บอกข้อจำกัดความรู้และการเดา | Knowledge-limit disclaimers and guesses |
| TH-28 | อธิบายซ้ำสิ่งที่ผู้อ่านรู้แล้ว | Re-explaining what the reader knows |

### English

| ID | Pattern |
|----|---------|
| EN-1 | Not X but Y |
| EN-2 | One-line closers and dramatic fragments |
| EN-3 | Sayings that sound deep |
| EN-4 | Staged run-up before the point |
| EN-5 | Arguing with no one |
| EN-6 | Forced triads |
| EN-7 | Repeated sentence openings |
| EN-8 | Dashes everywhere |
| EN-9 | Stacked qualifiers |
| EN-10 | Hidden actors |
| EN-11 | Overused AI words |
| EN-12 | Inflated significance |
| EN-13 | Sales language |
| EN-14 | Borrowed authority |
| EN-15 | Empty -ing riders |
| EN-16 | Avoiding "is" and "has" |
| EN-17 | Bold labels and decorative bold |
| EN-18 | Decorative headings |
| EN-19 | Curly quotes |
| EN-20 | Chatbot residue |
| EN-21 | Knowledge-limit disclaimers and guesses |
| EN-22 | Writing about the document |
| EN-23 | Re-explaining what the reader knows |

### Mixed Thai and English

| ID | Pattern |
|----|---------|
| MX-1 | English structure in Thai words |
| MX-2 | Formal Thai terms for everyday tech words |
| MX-3 | The same term in two forms |

## Responsible use

This skill edits wording. It does not check facts, and it does not make text "undetectable".

- **You are responsible for what you publish.** The skill keeps every claim in the source, including ones an AI made up, and lists them for you to check. Check them before you publish.
- **Follow the rules where you submit the text.** Many schools, journals, employers, and platforms require you to disclose AI use or ban it. This skill does not change those rules. Do not use it to hide AI use where disclosure is required.
- **No guarantee.** Readers and AI detectors may still judge the result as AI-written. The software is provided "as is", without warranty; see [LICENSE](LICENSE).
- **No data collection.** The skill is a set of instructions for your agent. It sends nothing anywhere by itself. Your text goes only to the AI service you already use, under that service's terms.

## Contributing

Found a Thai or English tell that is not listed? Open an issue with a real example and a rewrite. Before a pull request, run:

```bash
python3 scripts/validate-package.py
```

See [AGENTS.md](AGENTS.md) for the rules. By sending a pull request, you agree that your contribution is released under the MIT License of this project. Use only examples you wrote yourself or have the right to share, and remove personal data from them.

## Credits

This project adapts the skill structure, the workflow, and many English patterns from [Humanizer](https://github.com/blader/humanizer) by Siqi Chen (MIT), which is based on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). The Thai and mixed-language patterns are new. See [LICENSE](LICENSE).

This project is independent. It is not affiliated with or endorsed by the Humanizer authors, Wikipedia, or any AI company. Product names such as Claude, ChatGPT, Gemini, and Cursor are trademarks of their owners and are used here only to describe compatibility and test data.

## License

MIT
