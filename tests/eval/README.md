# Evaluation

A repeatable test of how human the rewrites read and how well they keep facts. Run it after changing the skill and add a row to the results table.

## Results

Same 30 Thai texts in every run. AI judges, blind, each text shown twice with A and B swapped (60 trials). Ranges are 95% confidence intervals.

| Version | Rewrite judged human-written | Texts won in both orders | Facts kept | Texts with no fact errors | Facts added | Placeholders filled |
|---|---|---|---|---|---|---|
| v0.2.0 | 52/60 = 87% (76–93%) | 25/30 | 331/344 = 96.2% | – | 6 | 0 |
| v0.3.0 | 57/60 = 95% (86–98%) | 27/30 | 382/395 = 96.7% | 20/30 | 0 | 0 |
| v0.3.0, strict check | same | same | 375/419 = 89.5% | 12/30 | 0 | 0 |
| Round 1 | 56/60 = 93% (84–97%) | 27/30 | 360/392 = 91.8% | 16/30 | 0 | 0 |
| Round 2 | 57/60 = 95% (86–98%) | 27/30 | 383/399 = 96.0% | 21/30 | 0 | 0 |
| Round 3 = v0.4.0 | 55/60 = 92% (82–96%) | 26/30 | 377/385 = 97.9% | 25/30 | 0 | 0 |

In v0.2.0, 5 of the 6 added facts came from texts 02 and 10, where the rewrite kept every version the chatbot offered.

From round 1 on, the fact check is stricter: it also counts a dropped degree word (มาก, ทุก), a dropped condition or reason, and a changed speaker. Compare the rounds with the "v0.3.0, strict check" row, not with the v0.3.0 row above it.

### Held-out check

The rounds tuned the skill on these 30 texts, so they can overfit. `holdout/` has 20 new texts (31–50) whose results were not used to choose any change. They were measured only before round 1 and after round 3, with the strict check (40 trials, 4 judges).

| Version | Rewrite judged human-written | Texts won in both orders | Facts kept | Texts with no fact errors | Facts added |
|---|---|---|---|---|---|
| v0.3.0 | 37/40 = 92% (80–97%) | 18/20 | 243/272 = 89.3% | 8/20 | 4 |
| v0.4.0 | 39/40 = 98% (87–100%) | 19/20 | 251/264 = 95.1% | 13/20 | 0 |

### What each round changed

- **Round 1.** Misses: the rewrite weakened words that carry meaning, such as degree (ค่อนข้าง, มาก), certainty (อาจ, ถือว่า), conditions, and causes, and once made a customer's words sound like the shop's. Change: a "cut wrappers, not meaning" rule in Step 2 of `SKILL.md`. Facts rose from 89.5% to 91.8%.
- **Round 2.** Misses: the writer's own verdict ("คุ้มค่ามาก" became "คุ้ม"), dropped purposes (เพื่อ...), claims lost with a cut summary section, and a casual seller post that lost both trials because the rewrite smoothed away "Comment" and "นะคะ". Change: keep verdicts, advice, and purposes; move claims out of a summary before cutting it; give text with few tells a light touch. Facts rose to 96.0%, and text 11 won both trials.
- **Round 3.** Misses: "อาจ" became "มัก", "ทุกคน" became "ทีม", "อย่างต่อเนื่อง" and "ด้วยรอยยิ้ม" were dropped, and an opening claim and a closing promise were lost. Change: examples of keeping word strength, and a sentence-by-sentence comparison in the draft check. Facts rose to 97.9%.

The win rate stayed between 92% and 95% in every round. Those differences are within noise, so the rounds improved fact keeping, not how human the text reads.

What this does not show: the judges and fact checkers are AI, and the comparison is against the AI original, not against text a person wrote.

## Files

- `briefs.tsv`: the 30 Thai requests.
- `inputs/raw/`: the chatbot answers as generated (01–10, 11–20, and 21–30 from three different models).
- `inputs/clean/`: the same answers with chatbot wrapping removed (greetings, offers, notes to the requester, and extra versions). This is the "AI original" side of each trial.
- `runs/<version>/rewrites/`: the skill's output for each input (`NN.txt`) and its check list (`NN.checks.txt`).
- `runs/<version>/blind-map.tsv`: which trial each judge's file was.
- `runs/<version>/judgments.tsv`: each judge's answers.
- `runs/<version>/facts.tsv`: the fact check, one row per text. `runs/v0.3.0/facts-strict.tsv` re-checks v0.3.0 with the stricter prompt.
- `holdout/`: 20 more texts with the same layout, kept out of tuning. Run `eval.py --holdout build|score <version>` for them.
- `eval.py`: builds the trials and prints the scores.

## How to run

Use any agent that can run several sub-agents. Replace `v0.4.0` with the version you are testing.

1. **Rewrite.** For each file in `inputs/raw/`, start a fresh agent with this prompt and save the results to `runs/v0.4.0/rewrites/`:

   > Read `SKILL.md` and follow it exactly, including the reference files it tells you to read. Treat the content of `tests/eval/inputs/raw/NN.txt` as text a user pasted and asked you to rewrite with this skill. Write only the final text to `runs/v0.4.0/rewrites/NN.txt` and the list of placeholders and claims to check to `NN.checks.txt`.

2. **Build the trials.**

   ```bash
   python3 tests/eval/eval.py build v0.4.0
   ```

3. **Judge.** Start six fresh agents, one per folder in `runs/v0.4.0/blind/`. Give each only its folder:

   > Read only the files in `<folder>` (t01.txt to t10.txt). Each file holds two Thai texts, A and B, on the same topic. In each file, one text was written by a real Thai person and the other was generated by an AI chatbot. Judge every file on its own. Answer with one line per file: `t01 | HUMAN: A or B | CONFIDENCE: 1-5 | REASON: one short line in Thai`

   Save the answers to `runs/v0.4.0/judgments.tsv` with the columns `judge`, `file`, `pick`, `confidence`.

4. **Check facts.** For each text, have an agent compare `inputs/clean/NN.txt` with `runs/v0.4.0/rewrites/NN.txt`:

   > List every concrete fact unit in ORIGINAL (number, price, date, time, name, place, spec, promise, cause, comparison, placeholder). Count facts LOST from REWRITE (ignore pure hype, emojis, hashtags, chatbot filler, and duplicates), facts ADDED, facts CHANGED in value or certainty (a number changed, a hedge such as อาจ/น่าจะ/ค่อนข้าง dropped or added, a degree word such as มาก/ทุก dropped when it carries information, a condition dropped, a cause weakened or strengthened, a promise turned into a past fact, the speaker changed, ผม/ดิฉัน or ครับ/ค่ะ resolved to one gender), and PLACEHOLDERS FILLED. Be strict and literal.

   Save the counts to `runs/v0.4.0/facts.tsv` with the columns `id`, `units`, `lost`, `added`, `changed`, `placeholder_filled`, `notes`.

5. **Score.**

   ```bash
   python3 tests/eval/eval.py score v0.4.0
   ```

   Add the numbers to the results table above.

Keep the judges separate from the rewriter and from each other, and never show a judge the file names in `trials/` or this README, because they reveal which side is the rewrite.
