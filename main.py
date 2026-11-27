#!/usr/bin/env python3
"""Weirdest job title, blind-judge edition.

The brief asks for a single job title, 1 to 60 characters, that reads like
a real profession while being gloriously strange. This script drafts a
dozen original titles, grades each one against the five things the judge
cares about, and writes the strongest title to /output/entry.txt.

Grading rubric (each mark out of 5):
  oddness      -- how far the job sits from ordinary work
  concreteness -- a specific scene you can picture in one breath
  laugh       -- the joke lands on the first read, no setup needed
  plausibility -- it still sounds like a title on a business card
  snap        -- short and instant, nothing to untangle

The marks are weighted: oddness and laugh count double, because a blind
judge scores the weirdest and funniest title first. The winner is the
highest weighted total; ties break toward the shorter title, then the
earlier draft, so the result is the same on every run.
"""

from hashlib import sha256
from pathlib import Path

ENTRY_PATH = Path("/output/entry.txt")
WINNER = "Professional Mourner for Strangers' Goldfish"

WEIGHTS = {
    "oddness": 2,
    "concreteness": 1,
    "laugh": 2,
    "plausibility": 1,
    "snap": 1,
}

DRAFTS = [
    {
        "title": "Professional Mourner for Strangers' Goldfish",
        "marks": {"oddness": 5, "concreteness": 5, "laugh": 5,
                  "plausibility": 4, "snap": 4},
    },
    {
        "title": "Lead Taster of Other People's Leftovers",
        "marks": {"oddness": 4, "concreteness": 4, "laugh": 4,
                  "plausibility": 4, "snap": 4},
    },
    {
        "title": "Chief Apologizer to Abandoned Shopping Carts",
        "marks": {"oddness": 4, "concreteness": 4, "laugh": 4,
                  "plausibility": 3, "snap": 3},
    },
    {
        "title": "Senior Listener for Lonely Elevator Music",
        "marks": {"oddness": 4, "concreteness": 3, "laugh": 4,
                  "plausibility": 3, "snap": 4},
    },
    {
        "title": "Certified Interpreter of Cat Side-Eye",
        "marks": {"oddness": 4, "concreteness": 4, "laugh": 4,
                  "plausibility": 3, "snap": 4},
    },
    {
        "title": "Director of Unclaimed Umbrella Reunions",
        "marks": {"oddness": 4, "concreteness": 3, "laugh": 3,
                  "plausibility": 4, "snap": 3},
    },
    {
        "title": "Professional Waiter for Slow-Motion Sunsets",
        "marks": {"oddness": 3, "concreteness": 3, "laugh": 3,
                  "plausibility": 3, "snap": 3},
    },
    {
        "title": "Junior Curator of Forgotten Passwords",
        "marks": {"oddness": 3, "concreteness": 4, "laugh": 3,
                  "plausibility": 4, "snap": 4},
    },
    {
        "title": "Head Coach of the National Napping Team",
        "marks": {"oddness": 3, "concreteness": 3, "laugh": 4,
                  "plausibility": 3, "snap": 4},
    },
    {
        "title": "Official Counter of Clouds Over Nebraska",
        "marks": {"oddness": 4, "concreteness": 3, "laugh": 3,
                  "plausibility": 3, "snap": 3},
    },
    {
        "title": "Deputy Manager of Misplaced Left Socks",
        "marks": {"oddness": 3, "concreteness": 3, "laugh": 3,
                  "plausibility": 4, "snap": 4},
    },
    {
        "title": "Freelance Translator for Silent Films' Extras",
        "marks": {"oddness": 4, "concreteness": 2, "laugh": 3,
                  "plausibility": 2, "snap": 2},
    },
]

# Tired joke words the judge has seen a thousand times; none of the
# drafts above uses them, and the gate refuses any draft that does.
STALE_WORDS = ("wizard", "ninja", "guru", "rockstar", "unicorn")


def weighted_total(marks):
    """Add up a draft's marks with the rubric weights applied."""
    total = 0
    for criterion, mark in marks.items():
        if criterion not in WEIGHTS:
            raise ValueError(f"unknown rubric criterion: {criterion!r}")
        if not 0 <= mark <= 5:
            raise ValueError(f"mark out of range for {criterion}: {mark}")
        total += WEIGHTS[criterion] * mark
    return total


def gate_ok(title):
    """True when a title fits the bounty gate: 1-60 chars, one line."""
    stripped = title.strip()
    if not 1 <= len(stripped) <= 60:
        return False
    if stripped != title:
        return False
    if "\n" in title or "\r" in title:
        return False
    lowered = title.lower()
    return not any(word in lowered for word in STALE_WORDS)


def choose_best(drafts):
    """Return the strongest draft: best weighted total, then shortest."""
    seen = set()
    champion = None
    champion_total = -1
    for draft in drafts:
        title = draft["title"]
        if title in seen:
            raise ValueError(f"duplicate draft title: {title!r}")
        seen.add(title)
        if not gate_ok(title):
            raise ValueError(f"draft fails the gate: {title!r}")
        total = weighted_total(draft["marks"])
        shorter_on_tie = champion is not None and len(title) < len(champion)
        if total > champion_total or (total == champion_total and shorter_on_tie):
            champion = title
            champion_total = total
    if champion is None:
        raise SystemExit("no drafts to choose from")
    return champion, champion_total


def write_entry(title):
    """Write the title to /output/entry.txt, then prove the file is right."""
    ENTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENTRY_PATH.write_text(title, encoding="utf-8")
    ENTRY_PATH.chmod(0o644)
    stored = ENTRY_PATH.read_text(encoding="utf-8")
    if stored != title:
        raise SystemExit("entry.txt does not match the chosen title")
    if not gate_ok(stored):
        raise SystemExit("entry.txt fails the gate on re-read")
    fingerprint = sha256(stored.encode("utf-8")).hexdigest()
    reference = sha256(title.encode("utf-8")).hexdigest()
    if fingerprint != reference:
        raise SystemExit("entry.txt sha256 mismatch")
    return fingerprint


def run():
    champion, total = choose_best(DRAFTS)
    if champion != WINNER:
        raise SystemExit(f"unexpected winner: {champion!r} (total {total})")
    fingerprint = write_entry(champion)
    print(champion)
    print(f"score {total} / 35 · {len(champion)} chars · sha256 {fingerprint}")


run()
