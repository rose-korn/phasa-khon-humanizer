#!/usr/bin/env python3
"""Build blind A/B trials for a run and score the judges' answers.

Usage:
  python3 tests/eval/eval.py build v0.4.0   # writes runs/v0.4.0/trials/ and runs/v0.4.0/blind/
  python3 tests/eval/eval.py score v0.4.0   # reads runs/v0.4.0/judgments.tsv and facts.tsv

See tests/eval/README.md for the whole procedure.
"""
import csv
import math
import random
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
IDS = [f"{i:02d}" for i in range(1, 31)]
JUDGES = 6
EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍←-⇿⌀-⏿]"
)


def clean(text):
    """Strip emojis so judges compare wording, not decoration."""
    text = EMOJI.sub("", text)
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def build(run):
    trials = run / "trials"
    blind = run / "blind"
    for d in (trials, blind):
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
    batches = defaultdict(list)
    for n, i in enumerate(IDS):
        ai = clean((HERE / "inputs" / "clean" / f"{i}.txt").read_text())
        rw = clean((run / "rewrites" / f"{i}.txt").read_text())
        for orient in ("AB", "BA"):
            a, b = (ai, rw) if orient == "AB" else (rw, ai)
            (trials / f"{i}{orient}.txt").write_text(
                f"=== ข้อความ A ===\n{a}\n\n=== ข้อความ B ===\n{b}\n"
            )
        # Each judge sees 10 different texts, with both orders mixed in.
        group = n // 10
        first, second = ("AB", "BA") if n % 2 == 0 else ("BA", "AB")
        batches[group].append(f"{i}{first}")
        batches[group + 3].append(f"{i}{second}")
    random.seed(7)
    with open(run / "blind-map.tsv", "w") as out:
        out.write("judge\tfile\ttrial\n")
        for g in sorted(batches):
            random.shuffle(batches[g])
            judge = f"j{g + 1}"
            (blind / judge).mkdir()
            for k, trial in enumerate(batches[g], 1):
                name = f"t{k:02d}"
                shutil.copy(trials / f"{trial}.txt", blind / judge / f"{name}.txt")
                out.write(f"{judge}\t{name}\t{trial}\n")
    print(f"Built 60 trials for {JUDGES} judges in {blind}")


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / d, (c + h) / d


def pct(k, n):
    lo, hi = wilson(k, n)
    return f"{k}/{n} = {k / n:.0%} (95% CI {lo:.0%}-{hi:.0%})"


def score(run):
    rows = list(csv.DictReader(open(run / "judgments.tsv"), delimiter="\t"))
    # Judges only see file names; blind-map.tsv says which trial each file was.
    trial_of = {
        (r["judge"], r["file"]): r["trial"]
        for r in csv.DictReader(open(run / "blind-map.tsv"), delimiter="\t")
    }
    for r in rows:
        r["trial"] = trial_of[(r["judge"], r["file"])]
    wins = defaultdict(list)
    for r in rows:
        # In an AB trial the rewrite is B; in a BA trial it is A.
        rewrite = "B" if r["trial"].endswith("AB") else "A"
        wins[r["trial"][:2]].append(r["pick"] == rewrite)
    k = sum(sum(v) for v in wins.values())
    n = sum(len(v) for v in wins.values())
    both = sum(all(v) for v in wins.values())
    print(f"Rewrite judged human-written: {pct(k, n)}")
    print(f"Texts won in both orders:     {pct(both, len(wins))}")
    lost = sorted(r["trial"] for r in rows if r["pick"] != ("B" if r["trial"].endswith("AB") else "A"))
    print(f"Trials lost: {', '.join(lost) or 'none'}")

    facts_file = run / "facts.tsv"
    if facts_file.exists():
        facts = list(csv.DictReader(open(facts_file), delimiter="\t"))
        units = sum(int(f["units"]) for f in facts)
        errors = sum(int(f[c]) for f in facts for c in ("lost", "added", "changed", "placeholder_filled"))
        clean_texts = sum(
            all(int(f[c]) == 0 for c in ("lost", "added", "changed", "placeholder_filled")) for f in facts
        )
        print(f"Facts kept unchanged:         {units - errors}/{units} = {(units - errors) / units:.1%}")
        print(f"Texts with no fact errors:    {clean_texts}/{len(facts)}")
        print(f"Facts added: {sum(int(f['added']) for f in facts)}, "
              f"placeholders filled: {sum(int(f['placeholder_filled']) for f in facts)}")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("build", "score"):
        sys.exit(__doc__)
    run_dir = HERE / "runs" / sys.argv[2]
    {"build": build, "score": score}[sys.argv[1]](run_dir)
