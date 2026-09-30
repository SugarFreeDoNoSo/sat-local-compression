# GitHub setup

Target: https://github.com/SugarFreeDoNoSo/sat-local-compression

This public repository hosts the working manuscript and its reproducible
research sources. Start from a fresh clone:

```sh
git clone https://github.com/SugarFreeDoNoSo/sat-local-compression.git
cd sat-local-compression
make verify
```

Install the dependencies listed in `docs/toolchain.md` before running
`make verify`. Read `AGENTS.md` and `docs/codex-handoff.md` before continuing
the research with an agent.

With an authenticated GitHub CLI, the issue-seeding command is idempotent:

```sh
python3 scripts/seed_issues.py
gh run list --repo SugarFreeDoNoSo/sat-local-compression
```

For each workflow run:

1. Check both research and manuscript jobs.
2. Download and inspect the manuscript artifact.
3. Keep theorem changes on focused branches with pull requests.
4. Consider requiring the two CI checks through a main-branch rule.

The initial backlog has six issues. Publication on a preprint service or
submission to a journal is outside this repository bootstrap.
