"""
sync_gfg.py
-----------
IMPORTANT — read this before wiring it up:

Unlike LeetCode, GeeksforGeeks has NO API (official or otherwise) that
exposes your submitted CODE. All that's publicly visible is your solved
problem *list* (name, link, difficulty) — not what you actually wrote or
when. So this script cannot fully replicate what sync_leetcode.py does.

What it CAN do, daily and for free:
  1. Hit a community-run GFG stats API to get your current solved list.
  2. Diff it against what we've seen before (scripts/state/gfg_state.json).
  3. For every newly-solved problem, create a stub folder + placeholder
     README row so the only manual step left is: paste your code into the
     stub file and commit. That turns "manually edit a markdown table"
     into "paste code, git commit" — most of the busywork is gone, but
     not all of it, because GFG simply doesn't hand out the code.

  The community API used here (geeks-for-geeks-api.vercel.app) is an
  unofficial, volunteer-hosted project — not something Anthropic or GFG
  operate or guarantee. If it's down or changes shape, this step just
  fails loudly and skips GFG for that run; LeetCode sync is unaffected.

Env vars required:
  GFG_USERNAME    your public GeeksforGeeks username
"""

import datetime
import os
import sys

import requests

from common import load_state, save_state, append_rows_to_readme, REPO_ROOT

STATS_API = "https://geeks-for-geeks-api.vercel.app/{username}"

DIFFICULTY_DISPLAY = {
    "school": "Easy",
    "basic": "Easy",
    "easy": "Easy",
    "medium": "Med",
    "hard": "Hard",
}


def fetch_solved_problems(username: str) -> list[dict]:
    """Returns a flat list of {"question": ..., "link": ..., "difficulty": ...}
    across all difficulty buckets the API groups them into."""
    resp = requests.get(STATS_API.format(username=username), timeout=30)
    resp.raise_for_status()
    data = resp.json()

    flat = []
    for bucket, payload in data.get("solvedStats", {}).items():
        for q in payload.get("questions", []):
            flat.append({"question": q["question"], "link": q["link"], "difficulty": bucket})
    return flat


def slugify(name: str) -> str:
    return name.strip().lower().replace(" ", "-").replace("/", "-")


def main() -> None:
    username = os.environ["GFG_USERNAME"]

    state = load_state("gfg")
    synced_links = set(state["synced_ids"])

    problems = fetch_solved_problems(username)
    today = datetime.date.today().isoformat()

    new_rows = []
    for p in problems:
        if p["link"] in synced_links:
            continue

        print(f"New solved problem found: {p['question']}")

        slug = slugify(p["question"])
        problem_dir = REPO_ROOT / "gfg-submission" / "dsa" / slug
        problem_dir.mkdir(parents=True, exist_ok=True)
        stub_path = problem_dir / "solution.py"
        if not stub_path.exists():
            stub_path.write_text(
                f"# TODO: paste your accepted GFG solution for:\n"
                f"# {p['question']} -> {p['link']}\n",
                encoding="utf-8",
            )

        difficulty = DIFFICULTY_DISPLAY.get(p["difficulty"].lower(), p["difficulty"])
        rel_path = f"./gfg-submission/dsa/{slug}/solution.py"
        # Date here is "the day we first noticed it solved", not the actual
        # submission date — GFG doesn't expose the latter publicly.
        row = (
            f"| {today} | Misc | [{p['question']}]({p['link']}) "
            f"| GFG | {difficulty} | [.py]({rel_path}) |"
        )
        new_rows.append(row)
        synced_links.add(p["link"])

    added = append_rows_to_readme(new_rows)
    state["synced_ids"] = sorted(synced_links)
    save_state("gfg", state)

    print(f"Done. Added {added} new stub row(s) to README.md — remember to paste in the code.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"sync_gfg.py failed (non-fatal, LeetCode sync still ran): {exc}", file=sys.stderr)
        # Exit 0 on purpose: GFG's community API is flaky by nature and we
        # don't want a GFG hiccup to mark the whole daily Action as failed.
        sys.exit(0)
