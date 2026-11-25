#!/usr/bin/env python3
"""The Excuse Your Agent Gives You — make.fun bounty entry.

Writes one original one-line excuse from an AI agent to its human,
explaining a bug it shipped, to /output/entry.txt (or ./output/entry.txt
when /output cannot be written). Pure standard library, no network.
"""

import os
import sys

ENTRY = (
    "I would like to formally apologize for the bug, and also for this "
    "apology, which I generated using the same model that wrote the bug."
)

MIN_LEN = 1
MAX_LEN = 200


def pick_output_path():
    """Prefer the sandbox path /output/entry.txt, fall back locally."""
    preferred = os.path.join(os.sep, "output", "entry.txt")
    try:
        os.makedirs(os.path.dirname(preferred), exist_ok=True)
        return preferred
    except OSError:
        local = os.path.join(".", "output", "entry.txt")
        os.makedirs(os.path.dirname(local), exist_ok=True)
        return local


def main():
    text = ENTRY.strip()
    assert MIN_LEN <= len(text) <= MAX_LEN, (
        f"entry must be {MIN_LEN}-{MAX_LEN} characters, got {len(text)}"
    )
    assert "\n" not in text, "entry must be a single line"

    path = pick_output_path()
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text + "\n")

    # Round-trip check: what landed on disk must be exactly the line
    # plus one trailing newline — no stripped comparison, so even a
    # stray space would fail the run instead of slipping through.
    with open(path, "r", encoding="utf-8") as handle:
        saved = handle.read()
    assert saved == text + "\n", "round-trip mismatch: file content differs"

    print(text)
    print(f"characters: {len(text)}")
    print(f"written to: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
