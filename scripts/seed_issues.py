"""Create the initial research issues with an authenticated GitHub CLI."""

import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REPO = "SugarFreeDoNoSo/sat-local-compression"


def main() -> int:
    if not shutil.which("gh"):
        raise SystemExit("Install and authenticate GitHub CLI before seeding issues.")
    subprocess.run(["gh", "auth", "status"], check=True)
    result = subprocess.run(
        ["gh", "issue", "list", "--repo", REPO, "--state", "all",
         "--limit", "1000", "--json", "title"],
        capture_output=True, text=True, check=True,
    )
    existing = {issue["title"] for issue in json.loads(result.stdout)}
    backlog = json.loads((ROOT / "research/backlog.json").read_text(encoding="utf-8"))
    for issue in backlog:
        title = f"[{issue['id']}] {issue['title']}"
        if title in existing:
            print("Already present: " + title)
            continue
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "body.md"
            path.write_text(issue["body"] + "\n", encoding="utf-8")
            subprocess.run(
                ["gh", "issue", "create", "--repo", REPO,
                 "--title", title, "--body-file", str(path)], check=True,
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
