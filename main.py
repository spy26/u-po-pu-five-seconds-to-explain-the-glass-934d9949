#!/usr/bin/env python3
"""Five Seconds to Explain the Glass — entry program.

Writes the single sentence a house cat would say in its own defence
after sweeping a glass off the table, to /output/entry.txt (or to
$MAKEFUN_OUTPUT_DIR/entry.txt when that variable is set).

Deterministic: the text is fixed, there is no network access, no
clock and no randomness, so every run writes byte-identical output.
"""

import os
import sys

ENTRY = "You talked to it more than me all week, so I removed the competition."


def validate_entry(text: str) -> None:
    """Enforce the competition gate before anything is written.

    The sealed scorer only accepts UTF-8 text of 1 to 200 characters
    that is not only whitespace; the judge only compares single
    sentences, so reject control characters and extra lines too.
    """
    if not text or text.strip() == "":
        raise ValueError("entry must not be empty or only whitespace")
    if len(text) > 200:
        raise ValueError(f"entry is {len(text)} characters, over the 200 limit")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        raise ValueError("entry must not contain control characters")


def main() -> int:
    validate_entry(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Read back and prove the file holds exactly the validated text:
    # a silent truncation or encoding surprise must fail loudly here,
    # never reach the grader as a different entry.
    with open(path, "rb") as f:
        written = f.read()
    if written != ENTRY.encode("utf-8"):
        print(f"error: {path} does not match the entry text", file=sys.stderr)
        return 1
    print(ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
