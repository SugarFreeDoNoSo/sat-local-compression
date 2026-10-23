"""Finite L03 certificates for a specified graph and read/unread cut.

The checker validates a whole-graph induced matching, not a general SAT or
circuit lower bound. Its width conclusion uses manuscript L03/L02. A separate
cover check certifies the greedy packing estimate; arbitrary smaller matchings
remain valid width certificates without that estimate. No exponential family
of witnesses is stored or enumerated by certificate verification.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
MAX_VERTICES = 256


def _integer(value: object, minimum: int, maximum: int, field: str) -> int:
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"{field} must be an integer from {minimum} to {maximum}.")
    return value


def _edge(value: object, n: int) -> tuple[int, int]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError("An edge must have exactly two vertex indices.")
    u = _integer(value[0], 0, n - 1, "edge endpoint")
    v = _integer(value[1], 0, n - 1, "edge endpoint")
    if u == v:
        raise ValueError("Loops are not permitted in a simple graph.")
    return min(u, v), max(u, v)


def _graph(n: int, edges: Iterable[tuple[int, int]], read: Iterable[int]):
    _integer(n, 0, MAX_VERTICES, "num_vertices")
    normalized = tuple(_edge(edge, n) for edge in edges)
    if len(normalized) != len(set(normalized)):
        raise ValueError("Repeated undirected edges are not permitted.")
    read = tuple(_integer(v, 0, n - 1, "read vertex") for v in read)
    if len(read) != len(set(read)):
        raise ValueError("Repeated read vertices are not permitted.")
    return tuple(sorted(normalized)), tuple(sorted(read))


@dataclass(frozen=True)
class MatchingCertificate:
    num_vertices: int
    edges: tuple[tuple[int, int], ...]
    read_vertices: tuple[int, ...]
    # Each pair is oriented from its read endpoint to its unread endpoint.
    matching: tuple[tuple[int, int], ...]

    def as_dict(self) -> dict:
        return {"schema_version": 1, "num_vertices": self.num_vertices,
                "edges": [list(edge) for edge in self.edges],
                "read_vertices": list(self.read_vertices),
                "matching": [list(edge) for edge in self.matching]}


@dataclass(frozen=True)
class VerifiedCertificate:
    matching_size: int
    width_lower_bound: int
    crossing_edges: int
    maximum_degree: int
    covers_crossing_edges: bool

    @property
    def packing_bound_verified(self) -> bool:
        """Coverage, not just a possibly accidental numerical inequality."""
        return self.covers_crossing_edges


def certificate_from_dict(value: object) -> MatchingCertificate:
    fields = {"schema_version", "num_vertices", "edges", "read_vertices", "matching"}
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError("Certificate fields do not match schema version 1.")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ValueError("Unsupported certificate schema.")
    if not all(isinstance(value[name], list) for name in ("edges", "read_vertices", "matching")):
        raise ValueError("Edges, read vertices and matching must be lists.")
    n = value["num_vertices"]
    edges, read = _graph(n, value["edges"], value["read_vertices"])
    matching = []
    for edge in value["matching"]:
        _edge(edge, n)  # Validate, but retain read-to-unread orientation.
        matching.append(tuple(edge))
    certificate = MatchingCertificate(n, edges, read, tuple(matching))
    verify_certificate(certificate)
    return certificate


def verify_certificate(certificate: MatchingCertificate) -> VerifiedCertificate:
    """Check the claim from graph data, independently of producer choices.

    Exact coverage condition: every crossing edge is incident to the union of
    open whole-graph neighborhoods of the endpoints of some chosen edge. Each
    union has at most 2*Delta vertices, hence covers at most 2*Delta^2 edges.
    A width-only certificate need not satisfy that extra condition.
    """
    n = certificate.num_vertices
    edges, read_tuple = _graph(n, certificate.edges, certificate.read_vertices)
    read = set(read_tuple)
    graph = set(edges)
    matching = certificate.matching
    endpoints = set()
    chosen = set()
    for pair in matching:
        edge = _edge(pair, n)
        a, b = pair
        if a not in read or b in read:
            raise ValueError("Every matching pair must be oriented read to unread.")
        if edge not in graph:
            raise ValueError("A matching pair is not a graph edge.")
        if a in endpoints or b in endpoints:
            raise ValueError("Matching edges must have disjoint endpoints.")
        endpoints.update(pair)
        chosen.add(edge)
    # Inspect ALL graph edges, including edges entirely within either cut side.
    induced = {edge for edge in graph if set(edge) <= endpoints}
    if induced != chosen:
        raise ValueError("Chosen endpoints do not induce exactly the matching in the whole graph.")
    degrees = [0] * n
    crossing = []
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1
        if (u in read) != (v in read):
            crossing.append((u, v))
    delta = max(degrees, default=0)
    # Deliberately compute the covering neighborhood from raw edges, rather than
    # reusing the producer's adjacency/deletion routine.
    covered_vertices = set()
    for u, v in edges:
        if u in endpoints:
            covered_vertices.add(v)
        if v in endpoints:
            covered_vertices.add(u)
    covers = all(u in covered_vertices or v in covered_vertices for u, v in crossing)
    q = len(matching)
    if covers and len(crossing) > 2 * delta * delta * q:
        raise ValueError("Internal inconsistency in the certified packing bound.")
    return VerifiedCertificate(q, 1 << q, len(crossing), delta, covers)


def greedy_certificate(num_vertices: int, edges: Iterable[tuple[int, int]],
                       read_vertices: Iterable[int]) -> MatchingCertificate:
    """Lexicographic greedy whole-graph induced matching on crossing edges."""
    edges, read_tuple = _graph(num_vertices, edges, read_vertices)
    read = set(read_tuple)
    neighbors = [set() for _ in range(num_vertices)]
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    remaining = {edge for edge in edges if (edge[0] in read) != (edge[1] in read)}
    matching = []
    while remaining:
        u, v = min(remaining)
        matching.append((u, v) if u in read else (v, u))
        forbidden = neighbors[u] | neighbors[v]
        remaining = {edge for edge in remaining if not forbidden.intersection(edge)}
    certificate = MatchingCertificate(num_vertices, edges, read_tuple, tuple(matching))
    result = verify_certificate(certificate)
    if not result.covers_crossing_edges:
        raise ValueError("Greedy construction left an uncovered crossing edge.")
    return certificate


def separating_assignments(certificate: MatchingCertificate, first: int,
                          second: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Construct two full inputs: different read prefixes, a common one-hot suffix.

    Masks choose subsets of the read endpoints of the certified matching. The
    return values have opposite predicate outputs; every other input bit is 0.
    Construction is polynomial in n+|E|+q, not enumeration of 2^q prefixes.
    """
    result = verify_certificate(certificate)
    _integer(first, 0, (1 << result.matching_size) - 1, "first prefix mask")
    _integer(second, 0, (1 << result.matching_size) - 1, "second prefix mask")
    if first == second:
        raise ValueError("Distinct prefix masks are required.")
    index = ((first ^ second) & -(first ^ second)).bit_length() - 1
    left = [0] * certificate.num_vertices
    right = [0] * certificate.num_vertices
    for i, (a, _) in enumerate(certificate.matching):
        left[a] = (first >> i) & 1
        right[a] = (second >> i) & 1
    unread = certificate.matching[index][1]
    left[unread] = right[unread] = 1
    return tuple(left), tuple(right)


def artifact_contents() -> str:
    # Finite demonstration certificates, not an all-orders/asymptotic proof.
    examples = [
        ("empty", 0, (), ()),
        ("matching-3", 6, ((0, 3), (1, 4), (2, 5)), (0, 1, 2)),
        ("read-side-obstruction", 6, ((0, 3), (1, 4), (2, 5), (0, 1)), (0, 1, 2)),
    ]
    for side in (4, 8, 16):
        edges = tuple((r * side + c, nr * side + nc)
                      for r in range(side) for c in range(side)
                      for nr, nc in ((r + 1, c), (r, c + 1))
                      if nr < side and nc < side)
        examples.append((f"grid-{side}x{side}-row-half", side * side, edges,
                         tuple(range(side * side // 2))))
    records = []
    for name, n, edges, read in examples:
        certificate = greedy_certificate(n, edges, read)
        result = verify_certificate(certificate)
        records.append({"name": name, "certificate": certificate.as_dict(),
                        "verified": {"matching_size": result.matching_size,
                                     "width_lower_bound": result.width_lower_bound,
                                     "crossing_edges": result.crossing_edges,
                                     "maximum_degree": result.maximum_degree,
                                     "covers_crossing_edges": result.covers_crossing_edges}})
    return json.dumps({"scope": "Finite cut-specific L03 certificates; not general circuit lower bounds.",
                       "examples": records}, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true", help="check committed demonstration certificates")
    modes.add_argument("--verify", type=Path, help="verify a single schema-v1 certificate JSON file")
    args = parser.parse_args()
    try:
        if args.verify:
            certificate = certificate_from_dict(json.loads(args.verify.read_text(encoding="utf-8")))
            result = verify_certificate(certificate)
            print(json.dumps(result.__dict__, sort_keys=True))
            print("Cut-specific L03 evidence; not formal verification or a general circuit lower bound.")
        else:
            path = ROOT / "data/matching_certificates.json"
            expected = artifact_contents()
            if args.check:
                if not path.is_file() or path.read_text(encoding="utf-8") != expected:
                    raise ValueError("Certificate data is stale; run experiments/matching_certificates.py.")
            else:
                path.write_text(expected, encoding="utf-8")
            print("Six finite induced-matching certificates checked; at most 256 vertices.")
    except (ValueError, TypeError, OSError) as error:
        print(f"Certificate verification failed: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
