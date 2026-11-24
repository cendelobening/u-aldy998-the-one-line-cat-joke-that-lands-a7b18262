"""Write one original one-line cat joke to entry.txt.

Pure Python standard library only. The joke is a single line of
1-200 characters, written atomically with mode 0644 and verified
by reading it back.
"""

import os
import sys

# v3 final: cut the padding word "then" -- the line now runs
# straight from setup to turn with no wind-up, per the brief's
# "no padding, no wind-up" rule. 99 chars.
JOKE = (
    "My cat left a dead mouse on my pillow and sat by the door "
    "like a DoorDash driver waiting for a tip."
)

MAX_CHARS = 200


def validate(line):
    """Check the entry line meets the gate: 1-200 chars, one line,
    no control characters, not only whitespace."""
    if not line or line != line.strip():
        raise ValueError("entry must not be empty or padded")
    if len(line) > MAX_CHARS:
        raise ValueError("entry is %d chars, over the 200 limit" % len(line))
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("entry contains control characters")
    return line


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    line = validate(JOKE)
    data = line.encode("utf-8")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    tmp = target + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.chmod(tmp, 0o644)
    os.replace(tmp, target)
    # Read back and verify bytes, UTF-8 and mode.
    with open(target, "rb") as fh:
        back = fh.read()
    if back != data:
        raise SystemExit("verification failed: bytes differ after write")
    if back.decode("utf-8") != line:
        raise SystemExit("verification failed: UTF-8 round-trip mismatch")
    mode = os.stat(target).st_mode & 0o777
    if mode != 0o644:
        raise SystemExit("verification failed: mode is %o, expected 644" % mode)
    print("wrote %d chars to %s" % (len(line), target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
