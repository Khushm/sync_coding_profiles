"""
common.py
---------
Shared helpers used by sync_leetcode.py and sync_gfg.py.

Responsibilities:
1. Read / write a small JSON "state" file per platform, so we never
   re-add a problem we've already synced (idempotency).
2. Insert new rows into the master README.md table without touching
   anything else in the file.

Nothing in this file talks to any external API — it only manipulates
local files. Keeping that split makes each piece easy to test on its
own.
"""

import json
import os
from pathlib import Path

# Root of the repo. GitHub Actions checks the repo out to $GITHUB_WORKSPACE;
# locally it just falls back to two levels up from this file (repo/scripts/common.py).
REPO_ROOT = Path(os.environ.get("GITHUB_WORKSPACE", Path(__file__).resolve().parent.parent))

README_PATH = REPO_ROOT / "README.md"
STATE_DIR = REPO_ROOT / "scripts" / "state"

# The exact header your table already uses. We search for this line to find
# where the table lives, so the script keeps working even if you add more
# prose above/below the table later.
TABLE_HEADER = "| Date (YYYY-MM-DD) | Topic | Problem Name | Platform | Difficulty | Solution |"
TABLE_DIVIDER = "| :--- | :--- | :--- | :--- | :--- | :--- |"


def load_state(platform: str) -> dict:
    """Load scripts/state/<platform>_state.json (creates an empty one if missing).

    Shape: {"synced_ids": ["...", "..."]}
    For LeetCode we store submission ids; for GFG we store problem slugs/links,
    since GFG has no submission id we can key off.
    """
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    path = STATE_DIR / f"{platform}_state.json"
    if not path.exists():
        return {"synced_ids": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(platform: str, state: dict) -> None:
    path = STATE_DIR / f"{platform}_state.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)
        f.write("\n")


def append_rows_to_readme(new_rows: list[str]) -> int:
    """Insert new markdown table rows right after the table's divider line,
    then re-sort the whole table by date (oldest first), so the log always
    reads top-to-bottom chronologically no matter what order platforms ran in.

    new_rows: list of already-formatted markdown rows, e.g.
        "| 2026-07-05 | Graph | [Name](url) | LeetCode | Med | [.py](path) |"

    Returns the number of rows actually added (0 if new_rows was empty —
    we skip touching the file entirely in that case, so a "nothing new
    today" run never creates a noisy empty commit).
    """
    if not new_rows:
        return 0

    text = README_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()

    try:
        header_idx = lines.index(TABLE_HEADER)
    except ValueError as exc:
        raise RuntimeError(
            "Couldn't find the table header in README.md — has the table "
            "format changed? Update TABLE_HEADER in scripts/common.py to match."
        ) from exc

    divider_idx = header_idx + 1  # divider line is always right after the header
    existing_rows_end = divider_idx + 1
    # Walk forward collecting existing data rows (anything starting with "|"
    # right after the divider) so we can merge + re-sort them.
    while existing_rows_end < len(lines) and lines[existing_rows_end].strip().startswith("|"):
        existing_rows_end += 1

    existing_rows = lines[divider_idx + 1: existing_rows_end]
    merged = existing_rows + new_rows

    # Each row's date is the first "cell" — sort lexically, which works
    # because YYYY-MM-DD sorts correctly as plain text.
    def row_date(row: str) -> str:
        return row.split("|")[1].strip()

    merged.sort(key=row_date)

    new_lines = lines[: divider_idx + 1] + merged + lines[existing_rows_end:]
    README_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return len(new_rows)


# LeetCode's API returns "Medium" but your table uses the shorter "Med" —
# this keeps new rows visually consistent with the ones you added by hand.
DIFFICULTY_DISPLAY = {
    "easy": "Easy",
    "medium": "Med",
    "hard": "Hard",
}

# Maps a submission's programming language to a file extension for the
# solution file we write to disk.
LANG_EXTENSION = {
    "python": "py",
    "python3": "py",
    "cpp": "cpp",
    "c": "c",
    "java": "java",
    "javascript": "js",
    "typescript": "ts",
    "csharp": "cs",
    "golang": "go",
    "kotlin": "kt",
    "swift": "swift",
    "rust": "rs",
    "ruby": "rb",
    "scala": "scala",
    "php": "php",
}
