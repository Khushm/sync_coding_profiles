"""
sync_leetcode.py
-----------------
Pulls your recent ACCEPTED LeetCode submissions and:
  1. Writes each solution's code to
     leetcode-submission/dsa-problems/<problem-slug>/solution.<ext>
  2. Appends a row to the README.md table for any submission we
     haven't synced before.

This uses LeetCode's *unofficial* GraphQL API (the same one
leetcode.com's own site calls). There is no official public API, so:
  - It can break if LeetCode changes their schema.
  - Getting your own submission CODE (not just the problem name)
    requires being "logged in" as you, via two cookie values
    (LEETCODE_SESSION and csrftoken) that you copy out of your browser.
    Treat these like passwords — they go into GitHub Actions **secrets**,
    never committed to the repo.
  - LEETCODE_SESSION expires every few weeks/months. When this script
    starts failing with 401/403 errors, just grab a fresh cookie value
    (steps are in the README section of the setup guide) and update the
    GitHub secret.

Env vars required (all set as GitHub Actions secrets):
  LEETCODE_USERNAME     your public LeetCode username
  LEETCODE_SESSION      cookie value
  LEETCODE_CSRF_TOKEN   cookie value
"""

import os
import sys
import requests

from common import (
    load_state,
    save_state,
    append_rows_to_readme,
    DIFFICULTY_DISPLAY,
    LANG_EXTENSION,
    REPO_ROOT,
)

GRAPHQL_URL = "https://leetcode.com/graphql"

# How many of your most-recent AC submissions to look at each run.
# 20 is plenty for a daily cron — you'd need to solve 20+ problems in
# a single day for this to miss one, and even then it'll catch up the
# next day since recentAcSubmissionList always shows the latest N.
RECENT_LIMIT = 20


def graphql_request(query: str, variables: dict, authed: bool = False) -> dict:
    """POST a GraphQL query to LeetCode. `authed=True` attaches your
    session cookies so LeetCode treats the request as coming from you
    (needed to read submission code, which is private-by-default)."""
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com",
    }
    if authed:
        session = os.environ["LEETCODE_SESSION"]
        csrf = os.environ["LEETCODE_CSRF_TOKEN"]
        headers["Cookie"] = f"LEETCODE_SESSION={session}; csrftoken={csrf}"
        headers["x-csrftoken"] = csrf

    resp = requests.post(
        GRAPHQL_URL, json={"query": query, "variables": variables}, headers=headers, timeout=30
    )
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(f"LeetCode GraphQL error: {data['errors']}")
    return data["data"]


def fetch_recent_accepted(username: str) -> list[dict]:
    """Public endpoint — no auth needed. Returns id/title/slug/timestamp/lang
    for your most recent accepted submissions."""
    query = """
    query recentAcSubmissions($username: String!, $limit: Int!) {
      recentAcSubmissionList(username: $username, limit: $limit) {
        id
        title
        titleSlug
        timestamp
        lang
      }
    }
    """
    data = graphql_request(query, {"username": username, "limit": RECENT_LIMIT})
    return data["recentAcSubmissionList"]


def fetch_submission_code(submission_id: str) -> str:
    """Private endpoint — requires your session cookie. Returns the actual
    source code you submitted for this submission id."""
    query = """
    query submissionDetails($submissionId: Int!) {
      submissionDetails(submissionId: $submissionId) {
        code
      }
    }
    """
    data = graphql_request(query, {"submissionId": int(submission_id)}, authed=True)
    details = data.get("submissionDetails")
    if not details:
        raise RuntimeError(
            f"No submissionDetails returned for id={submission_id} — "
            "your LEETCODE_SESSION / LEETCODE_CSRF_TOKEN secret is probably stale."
        )
    return details["code"]


def fetch_question_metadata(title_slug: str) -> dict:
    """Public endpoint — difficulty + topic tags for a problem, used to fill
    in the "Topic" and "Difficulty" columns of the README table."""
    query = """
    query questionData($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        difficulty
        topicTags {
          name
        }
      }
    }
    """
    data = graphql_request(query, {"titleSlug": title_slug})
    return data["question"]


def main() -> None:
    username = os.environ["LEETCODE_USERNAME"]

    state = load_state("leetcode")
    synced_ids = set(state["synced_ids"])

    submissions = fetch_recent_accepted(username)
    # Oldest-first, so if there are several new ones today they land in the
    # README in the order you actually solved them.
    submissions.sort(key=lambda s: int(s["timestamp"]))

    new_rows = []
    for sub in submissions:
        if sub["id"] in synced_ids:
            continue  # already synced on a previous run

        print(f"New submission found: {sub['title']} ({sub['lang']})")

        code = fetch_submission_code(sub["id"])
        meta = fetch_question_metadata(sub["titleSlug"])

        ext = LANG_EXTENSION.get(sub["lang"], "txt")
        difficulty = DIFFICULTY_DISPLAY.get(meta["difficulty"].lower(), meta["difficulty"])
        topic = meta["topicTags"][0]["name"] if meta["topicTags"] else "Misc"

        # Write the solution file to disk.
        problem_dir = REPO_ROOT / "leetcode-submission" / "dsa-problems" / sub["titleSlug"]
        problem_dir.mkdir(parents=True, exist_ok=True)
        solution_path = problem_dir / f"solution.{ext}"
        solution_path.write_text(code, encoding="utf-8")

        # Build the README row in exactly your existing table format.
        import datetime
        date_str = datetime.datetime.utcfromtimestamp(int(sub["timestamp"])).strftime("%Y-%m-%d")
        problem_url = f"https://leetcode.com/problems/{sub['titleSlug']}/description/"
        rel_solution_path = f"./leetcode-submission/dsa-problems/{sub['titleSlug']}/solution.{ext}"

        row = (
            f"| {date_str} | {topic} | [{sub['title']}]({problem_url}) "
            f"| LeetCode | {difficulty} | [.{ext}]({rel_solution_path}) |"
        )
        new_rows.append(row)
        synced_ids.add(sub["id"])

    added = append_rows_to_readme(new_rows)
    state["synced_ids"] = sorted(synced_ids)
    save_state("leetcode", state)

    print(f"Done. Added {added} new row(s) to README.md.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 — surface any failure clearly in Action logs
        print(f"sync_leetcode.py failed: {exc}", file=sys.stderr)
        sys.exit(1)
