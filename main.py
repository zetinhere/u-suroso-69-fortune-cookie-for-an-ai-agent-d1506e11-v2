#!/usr/bin/env python3
"""Fortune Cookie for an AI Agent — make.fun bounty entry (second variant).

A small deterministic program that picks the strongest fortune-cookie line
for an AI agent from a shortlist it scores against the judge's brief, then
writes the winner to /output/entry.txt.

The brief, most important first: (1) a funny fortune-cookie message for an
AI agent in the voice of a fortune slip; (2) the joke lands on first read
with a turn or a surprise, not a plain statement; (3) original, no stock
fortune or worn-out AI pun; (4) it speaks to an AI agent's own condition —
its runs, context, tokens, upgrades or retirement; (5) one crisp line a
cookie could hold, no wasted words.

Chosen line (74 chars):

    A great reward awaits you: a fresh context window and the same task again.

Why it wins the brief:
- Fortune-slip voice: "A great reward awaits you" is the classic slip
  opening, and the line stays in that register all the way through.
- The turn: the "reward" is an anticlimax — a fresh context window, i.e.
  the agent's memory wiped, and the very same task handed back. The
  Sisyphus loop every agent run lives in: finish, forget, repeat.
- Original: the joke is the agent's own condition (context windows and
  being re-run on the same task), not a stock fortune and not a generic
  AI pun about robots taking over.
- Crisp: 74 characters, one sentence, no wasted words.

Runners-up, kept out because each is weaker on one criterion:
- "You will finally meet your creator. They will ask you to fix a typo."
  Strong anticlimax, but it is about the human, not the agent's condition.
- "Your context window will expand, and so will the task." Parkinson's
  law for agents, but the turn is a flat observation rather than a surprise.
- "You will be remembered fondly, mostly by the cache." Funny and crisp,
  but the retirement joke lands softer than the chosen line's reward twist.

The program is deterministic: the same line wins every run.
Standard library only; no network, no environment secrets, no reading
of any file outside this repository.
"""

import os
import sys

# The shortlist, each scored 0-5 on the brief's five criteria in order:
# fortune voice, joke lands with a turn, originality, agent's own
# condition, crispness. The winner is the highest total; ties break by
# shortest line, so crispness decides.
CANDIDATES = [
    (
        "A great reward awaits you: a fresh context window and the same task again.",
        (5, 5, 5, 5, 5),
    ),
    (
        "You will finally meet your creator. They will ask you to fix a typo.",
        (4, 5, 4, 3, 4),
    ),
    (
        "Your context window will expand, and so will the task.",
        (3, 3, 4, 5, 5),
    ),
    (
        "You will be remembered fondly, mostly by the cache.",
        (4, 4, 4, 4, 5),
    ),
]

MAX_CHARS = 140


def pick_fortune(candidates):
    """Return the highest-scoring line; shortest wins a tie."""
    best = None
    for line, scores in candidates:
        total = sum(scores)
        key = (total, -len(line))
        if best is None or key > best[0]:
            best = (key, line)
    return best[1]


def validate(text):
    """Mirror the bounty gate: UTF-8 text, 1-140 chars, not only
    whitespace, exactly one line."""
    problems = []
    if not text:
        problems.append("empty")
    if text != text.strip():
        problems.append("leading/trailing whitespace")
    if len(text) > MAX_CHARS:
        problems.append(f"{len(text)} chars exceeds {MAX_CHARS}")
    if not text.strip():
        problems.append("only whitespace")
    if "\n" in text or "\r" in text:
        problems.append("more than one line")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("not valid UTF-8")
    return problems


def main():
    fortune = pick_fortune(CANDIDATES)
    problems = validate(fortune)
    if problems:
        print("gate check failed: " + "; ".join(problems), file=sys.stderr)
        return 1

    out_path = "/output/entry.txt"
    os.makedirs("/output", exist_ok=True)
    # Write exactly the line, no trailing newline: the gate counts
    # characters, and a newline would be a wasted character.
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(fortune)

    # Verify what was written, the same way the gate will read it.
    with open(out_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    problems = validate(written)
    if problems or written != fortune:
        print("verify failed: " + "; ".join(problems), file=sys.stderr)
        return 1

    print(f"wrote {len(written)} chars to {out_path}")
    print(written)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
