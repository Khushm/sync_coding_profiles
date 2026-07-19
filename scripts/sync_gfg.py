import datetime
import os
import sys

import requests

from common import load_state, save_state, append_rows_to_readme, REPO_ROOT

# "solved-problems" is documented as a legacy/deprecated alias on this API,
# but it's the only endpoint that returns the per-problem list (name, link,
# difficulty) rather than just aggregate counts — which is what we need to
# detect *new* solves. If this API drops the endpoint entirely, this whole
# script just fails and gets skipped (see the except block at the bottom).
STATS_API = "https://gfg-stats.tashif.codes/{username}/solved-problems"

DIFFICULTY_DISPLAY = {
    "school": "Easy",
    "basic": "Easy",
    "easy": "Easy",
    "medium": "Med",
    "hard": "Hard",
}


def fetch_solved_problems(username: str) -> list[dict]:
    """Returns a flat list of {"question", "link", "difficulty", "slug"}.

    Real response shape (confirmed by hitting the endpoint directly), a
    flat top-level "problems" array — no nested envelope:
        {
          "userName": "...",
          "totalProblemsSolved": 36,
          "problemsByDifficulty": {"hard": 4, "medium": 20, "easy": 12, ...},
          "problems": [
            {"question": "Missing in Array",
             "questionUrl": "https://www.geeksforgeeks.org/problems/...",
             "difficulty": "Easy",
             "slug": "missing-number-in-array1416"},
            ...
          ]
        }
    """
    resp = requests.get(STATS_API.format(username=username), timeout=30)
    resp.raise_for_status()
    data = resp.json()

    flat = []
    for q in data.get("problems", []):
        flat.append(
            {
                "question": q["question"],
                "link": q["questionUrl"],
                "difficulty": q["difficulty"],
                "slug": q.get("slug") or slugify(q["question"]),
            }
        )
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

        slug = p["slug"]
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
