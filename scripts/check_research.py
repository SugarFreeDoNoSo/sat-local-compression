"""Check research metadata and references; this does not verify proofs."""

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
register = json.loads((ROOT / "research/claims.json").read_text(encoding="utf-8"))
claims = register["claims"]
ids = [c["id"] for c in claims]
assert len(ids) == len(set(ids)), "Duplicate claim IDs."
allowed = {"expository-proved", "conditional-literature", "open", "finite-experiment"}
tex = "\n".join(
    p.read_text(encoding="utf-8") for p in sorted((ROOT / "paper").rglob("*.tex"))
)
bib = (ROOT / "paper/references.bib").read_text(encoding="utf-8")
bibkeys = set(re.findall(r"@\w+\{([^,]+),", bib))
labels = re.findall(r"\\label\{([^}]+)\}", tex)
assert len(labels) == len(set(labels)), "Duplicate LaTeX labels."
labelset = set(labels)
for group in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}", tex):
    for key in group.split(","):
        assert key.strip() in bibkeys, f"Missing bibliography entry: {key}"
for label in re.findall(r"\\(?:ref|eqref)\{([^}]+)\}", tex):
    assert label in labelset, f"Missing reference label: {label}"
for claim in claims:
    assert claim["status"] in allowed, f"Invalid status: {claim['id']}"
    assert claim["statement"] and claim["scope"], f"Unspecified claim: {claim['id']}"
    if claim.get("label"):
        assert claim["label"] in labelset, f"Missing claim label: {claim['id']}"
    for key in claim.get("sources", []):
        assert key in bibkeys, f"Unknown source: {key}"
    for dependency in claim["depends_on"]:
        assert dependency in ids, f"Unknown dependency: {dependency}"

by_id = {c["id"]: c for c in claims}
complete = set()


def visit(claim_id: str, active: set[str]) -> None:
    if claim_id in complete:
        return
    assert claim_id not in active, f"Cyclic dependency at {claim_id}"
    for dependency in by_id[claim_id]["depends_on"]:
        visit(dependency, active | {claim_id})
    complete.add(claim_id)


for claim_id in ids:
    visit(claim_id, set())

statements = re.findall(
    r"\\begin\{(theorem|proposition|lemma|corollary|conjecture)\}"
    r"\[([\s\S]*?)\]\s*\\label\{([^}]+)\}",
    tex,
)
for environment, title, label in statements:
    match = re.search(r"\\claimid\{([^}]+)\}", title)
    assert match, f"Unregistered mathematical statement: {label}"
    claim_id = match.group(1)
    assert claim_id in by_id, f"Missing register entry: {claim_id}"
    assert by_id[claim_id]["label"] == label, f"Claim-label mismatch: {claim_id}"
    status = by_id[claim_id]["status"]
    assert (environment == "conjecture") == (status == "open"), (
        f"Conjecture status mismatch: {claim_id}"
    )

statement_ids = {re.search(r"\\claimid\{([^}]+)\}", t).group(1) for _, t, _ in statements}
expected = {c["id"] for c in claims if c["status"] in {"expository-proved", "open"}}
assert statement_ids == expected, "Statement register and manuscript are out of sync."
print(f"Research metadata verified: {len(claims)} claims, {len(bibkeys)} bibliography entries.")
print("This is a consistency check, not mathematical proof verification.")
