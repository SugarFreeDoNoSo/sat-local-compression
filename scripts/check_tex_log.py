"""Reject unresolved references and material LaTeX rendering warnings."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "build/paper/main.log"
if not path.exists():
    raise SystemExit("Missing LaTeX log; run make pdf first.")
log = path.read_text(encoding="utf-8", errors="replace")
if "Output written on " not in log:
    raise SystemExit("Incomplete LaTeX log; rebuild with make clean && make verify.")
patterns = [
    r"Overfull \\[hv]box",
    r"LaTeX Warning: (?:Citation|Reference).*undefined",
    r"There were undefined references",
    r"Label .* multiply defined",
    r"There were multiply-defined labels",
    r"Missing character:",
    r"Fatal error",
]
failures = [line for line in log.splitlines() if any(re.search(p, line) for p in patterns)]
if failures:
    raise SystemExit("LaTeX quality gate failed:\n" + "\n".join(failures))
print("LaTeX log: no unresolved references, overfull boxes, or missing characters.")
