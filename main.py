# The Weirdest Job Title: Blind Judge Showdown — make.fun bounty
# u-rusdyxbt-weirdest-job-title-blind-judge-showdown-552d7922
#
# The program writes one job title (1-60 characters) to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a weird job title, a few words naming an odd job
#   2. stranger than ordinary work, with a gloriously odd twist
#   3. funny on the first read, the twist landing at once
#   4. sounds like a real job, specific enough to picture the person
#   5. reads instantly, short enough to take in at a glance
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: weird 10, strange 9, funny 9, real 9, instant 9 = 46
    ("Professional Mourner for Strangers' Goldfish", 46),
    # score: weird 9, strange 9, funny 8, real 8, instant 9 = 43
    ("Senior Penguin Accountant, Iceberg Division", 43),
    # score: weird 9, strange 8, funny 9, real 8, instant 8 = 42
    ("Professional Queue Stander for People Who Hate Queues", 42),
    # score: weird 9, strange 9, funny 8, real 7, instant 8 = 41
    ("Chief Executive Officer of Other People's Dreams", 41),
    # score: weird 8, strange 9, funny 8, real 7, instant 9 = 41
    ("Certified Cloud Shaper, Cumulus Department", 41),
    # score: weird 8, strange 8, funny 8, real 8, instant 9 = 41
    ("Senior Vice President of Lost Socks", 41),
    # score: weird 8, strange 8, funny 8, real 8, instant 9 = 41
    ("Professional Apologizer to Houseplants", 41),
]

# The gate requires 1-60 characters of non-whitespace UTF-8 text.
BANNED_CLICHES = ("wizard", "ninja", "guru", "rockstar", "unicorn")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 60, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a worn joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    title = pick(CANDIDATES)
    import hashlib
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(title)
    os.chmod("/output/entry.txt", 0o644)
    # Verify what was actually written: the gate reads this file, not stdout.
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    assert written == title, "entry.txt differs from the chosen title"
    assert 1 <= len(written.strip()) <= 60, "entry.txt outside the gate"
    assert "\n" not in written.strip(), "entry.txt must be one line"
    digest = hashlib.sha256(written.encode("utf-8")).hexdigest()
    expected = hashlib.sha256(title.encode("utf-8")).hexdigest()
    assert digest == expected, "entry.txt sha256 mismatch"
    print(title)
    print(f"sha256: {digest} ({len(written)} chars)")


if __name__ == "__main__":
    main()
