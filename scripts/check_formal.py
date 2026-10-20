#!/usr/bin/env python3
"""Build L02 with the pinned Lean toolchain and audit theorem axiom closures."""

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "formal"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
THEOREMS = {
    "ResidualWidths." + name
    for name in (
        "mem_allWords_iff",
        "distinctCount_le_of_fiber_imp",
        "equal_state_equal_residual",
        "residualCount_le_reachableWidth",
        "canonical_correct",
        "canonical_width",
        "canonical_attains_all_cuts",
        "residual_width_characterization",
        "atLength_supported",
        "atLength_agrees",
        "initial_width",
        "initial_residual_count",
        "terminal_residual_count",
        "residual_eq_iff_on_valid_suffix",
        "valid_suffix_length_iff",
        "reachable_step",
        "length_allWords",
        "reachableWidth_le_prefixes",
    )
}


def parse_audit(output, expected=THEOREMS):
    """Require real Lean JSON diagnostics for every expected declaration."""
    found = {}
    for line in output.splitlines():
        if not line.strip():
            continue
        message = json.loads(line)
        if message.get("severity") != "information":
            raise ValueError(f"Lean diagnostic: {message}")
        data = message.get("data", "")
        match = re.fullmatch(r"'([^']+)' depends on axioms: \[(.*?)\]", data, re.S)
        no_axioms = re.fullmatch(r"'([^']+)' does not depend on any axioms", data)
        if match:
            name, axioms_text = match.groups()
            axioms = {a.strip() for a in axioms_text.split(",") if a.strip()}
        elif no_axioms:
            name, axioms = no_axioms.group(1), set()
        else:
            raise ValueError(f"Unexpected axiom-audit output: {data}")
        if name not in expected or name in found:
            raise ValueError(f"Unexpected or repeated declaration: {name}")
        forbidden = axioms - ALLOWED_AXIOMS
        if forbidden:
            raise ValueError(f"{name} depends on forbidden axioms: {sorted(forbidden)}")
        found[name] = sorted(axioms)
    if set(found) != set(expected):
        raise ValueError(f"Missing declarations: {sorted(set(expected) - set(found))}")
    return found


def run(command, log):
    result = subprocess.run(command, cwd=FORMAL, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log.write_text(result.stdout, encoding="utf-8")
    if result.returncode:
        print(result.stdout, end="")
        raise RuntimeError(f"Command failed ({result.returncode}); see {log}")
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lake", default="lake", help="Lake executable (default: PATH)")
    args = parser.parse_args()
    logs = ROOT / "build" / "formal"
    logs.mkdir(parents=True, exist_ok=True)
    # No failure in this invocation should leave an earlier success report.
    (logs / "verification.json").unlink(missing_ok=True)
    resolved = shutil.which(args.lake)
    if resolved is None:
        raise ValueError("Lake not found. Run python3 scripts/setup_lean.py; see formal/README.md")
    # Preserve argv[0] for elan's symlink-based `lake` shim.
    lake = str(Path(resolved).absolute())
    pin = json.loads((FORMAL / "toolchain.json").read_text(encoding="utf-8"))
    expected_pin = f"leanprover/lean4:v{pin['version']}"
    for path in (ROOT / "lean-toolchain", FORMAL / "lean-toolchain"):
        if path.read_text(encoding="utf-8").strip() != expected_pin:
            raise ValueError(f"Toolchain pin mismatch in {path}")
    version = run([lake, "env", "lean", "--version"], logs / "toolchain.log").strip()
    if f"version {pin['version']}," not in version or f"commit {pin['commit']}," not in version:
        raise ValueError(f"Expected pinned Lean {pin['version']} / {pin['commit']}; got {version}")
    run([lake, "build"], logs / "build.log")
    audit = run([lake, "env", "lean", "-DwarningAsError=true", "-Dpp.fullNames=true",
                 "--json", "AxiomAudit.lean"],
                logs / "axioms.jsonl")
    found = parse_audit(audit)
    report = {"claim": "L02", "lean": version, "theorem_axioms": found,
              "allowed_axioms": sorted(ALLOWED_AXIOMS)}
    (logs / "verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"L02 verified with Lean {pin['version']}: {len(found)} theorem axiom closures checked.")
    print(f"Evidence: {logs.relative_to(ROOT)}/verification.json")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, OSError) as error:
        print(f"Formal verification failed: {error}", file=sys.stderr)
        sys.exit(1)
