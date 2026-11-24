"""The Houseplant Out-of-Office.

A tiny program whose whole job is to deliver one out-of-office
auto-reply written as if a houseplant sent it. The reply is short
on purpose: the judge only accepts 1 to 120 characters, and a
houseplant with no water has no time for long emails anyway.

The line itself is the entry. Everything else here is plumbing:
pick the output directory the grader provides, check the line
fits the gate, and write it out.
"""

import os
import sys


# The entry: one out-of-office auto-reply from the plant on the
# windowsill. It turned the sender's email into oxygen and let it
# drift out the window, so the sender is asked to resend it --
# with water, this time.
REPLY = (
    "Out of office. I turned your email into oxygen "
    "and let it out the window. Please resend it, with water."
)

MAX_CHARS = 120


def output_dir():
    """Return the directory the grader wants the entry written to."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if chosen:
        return chosen
    return os.path.join(os.getcwd(), "output")


def looks_like_auto_reply(text):
    """Sanity check: the line must read as an out-of-office reply.

    The judge's first criterion is that the text reads as an
    out-of-office auto-reply a houseplant would send, and anything
    else loses to any auto-reply on the subject. So the program
    refuses to ship a line that does not open like one.
    """
    head = text.strip().lower()
    return head.startswith("out of office")


def main():
    text = REPLY
    if not looks_like_auto_reply(text):
        print("reply does not read as an out-of-office message",
              file=sys.stderr)
        return 1
    if not text.strip():
        print("refusing to write an empty reply", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(
            "reply is %d characters, over the %d limit"
            % (len(text), MAX_CHARS),
            file=sys.stderr,
        )
        return 1
    folder = output_dir()
    os.makedirs(folder, exist_ok=True)
    target = os.path.join(folder, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    print("wrote %d characters to %s" % (len(text), target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
