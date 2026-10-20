"""Fetch or reuse the pinned Linux Lean release without a system installation.

Uses the Python standard library and the external zstd decompressor. The final
stdout line is the absolute Lake executable path; diagnostics go to stderr.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import platform
import posixpath
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, build_opener


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "formal/toolchain.json"
STAMP = ".verified-toolchain.json"
MAX_UNPACKED_BYTES = 12 * 1024**3
MAX_MEMBERS = 100_000


def load_manifest() -> dict:
    """Check the tracked pin and canonical official download location."""
    info = json.loads(MANIFEST.read_text(encoding="utf-8"))
    version = info["version"]
    if info.get("schema_version") != 1 or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Unsupported toolchain manifest or nonstable version")
    archive_root = f"lean-{version}-linux"
    archive = archive_root + ".tar.zst"
    expected_url = (
        "https://github.com/leanprover/lean4/releases/download/"
        f"v{version}/{archive}"
    )
    if (info["archive_root"] != archive_root or info["archive"] != archive
            or info["url"] != expected_url
            or info["toolchain"] != f"leanprover/lean4:v{version}"
            or info["target"] != "x86_64-unknown-linux-gnu"):
        raise ValueError("Toolchain manifest does not describe the official Linux asset")
    if not re.fullmatch(r"[0-9a-f]{64}", info["sha256"]):
        raise ValueError("Invalid archive SHA256 in toolchain manifest")
    if not re.fullmatch(r"[0-9a-f]{40}", info["commit"]):
        raise ValueError("Invalid Lean commit in toolchain manifest")
    if type(info["size_bytes"]) is not int or not 0 < info["size_bytes"] < 2 * 1024**3:
        raise ValueError("Invalid archive size in toolchain manifest")
    if (ROOT / "lean-toolchain").read_text(encoding="utf-8").strip() != info["toolchain"]:
        raise ValueError("lean-toolchain and formal/toolchain.json disagree")
    return info


def verify_archive(archive: Path, info: dict) -> None:
    if not archive.is_file() or archive.stat().st_size != info["size_bytes"]:
        raise ValueError(f"Archive size differs from the pin: {archive}")
    digest = hashlib.sha256()
    with archive.open("rb") as source:
        for chunk in iter(lambda: source.read(4 * 1024**2), b""):
            digest.update(chunk)
    if digest.hexdigest() != info["sha256"]:
        raise ValueError(f"Archive SHA256 differs from the pin: {archive}")


class HTTPSRedirectsOnly(HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, new_url):
        if urlsplit(new_url).scheme != "https":
            raise ValueError("Refusing a non-HTTPS release redirect")
        return super().redirect_request(request, response, code, message, headers, new_url)


def download_archive(directory: Path, info: dict) -> Path:
    """Use inherited proxy/CA settings; authenticate bytes with the tracked digest."""
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / info["archive"]
    if target.exists():
        verify_archive(target, info)
        return target
    opener = build_opener(HTTPSRedirectsOnly())
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=directory, suffix=".part", delete=False) as out:
            temporary = Path(out.name)
            total = 0
            next_report = 64 * 1024**2
            with opener.open(info["url"], timeout=30) as response:
                while chunk := response.read(4 * 1024**2):
                    total += len(chunk)
                    if total > info["size_bytes"]:
                        raise ValueError("Downloaded release exceeds its pinned size")
                    out.write(chunk)
                    if total >= next_report:
                        print(f"Lean archive: {total}/{info['size_bytes']} bytes", file=sys.stderr)
                        next_report += 64 * 1024**2
        verify_archive(temporary, info)
        temporary.replace(target)
        return target
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def checked_parts(name: str, archive_root: str) -> tuple[str, ...]:
    path = PurePosixPath(name)
    if (not name or "\\" in name or "\x00" in name or path.is_absolute()
            or ".." in path.parts or not path.parts or path.parts[0] != archive_root):
        raise ValueError(f"Unsafe archive member: {name!r}")
    return path.parts


def extract_archive(archive: Path, staging: Path, info: dict) -> Path:
    """Extract files and internal relative symlinks, never through a symlink."""
    if shutil.which("zstd") is None:
        raise ValueError("zstd is required to decompress the official .tar.zst release")
    process = subprocess.Popen(
        ["zstd", "--decompress", "--stdout", str(archive)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    total = 0
    count = 0
    try:
        with tarfile.open(fileobj=process.stdout, mode="r|") as payload:
            for member in payload:
                count += 1
                total += member.size
                if count > MAX_MEMBERS or total > MAX_UNPACKED_BYTES:
                    raise ValueError("Toolchain archive exceeds extraction limits")
                parts = checked_parts(member.name, info["archive_root"])
                parent = staging
                for part in parts[:-1]:
                    parent = parent / part
                    if parent.is_symlink():
                        raise ValueError("Archive member has a symlink ancestor")
                    parent.mkdir(exist_ok=True)
                target = parent / parts[-1]
                if target.is_symlink() or (target.exists() and not member.isdir()):
                    raise ValueError("Archive contains an overlapping member")
                if member.isdir():
                    target.mkdir(exist_ok=True)
                    target.chmod(0o755)
                elif member.isfile():
                    source = payload.extractfile(member)
                    if source is None:
                        raise ValueError("Archive file has no payload")
                    with source, target.open("xb") as out:
                        shutil.copyfileobj(source, out, 1024**2)
                    target.chmod(0o755 if member.mode & 0o111 else 0o644)
                elif member.issym():
                    link = member.linkname
                    if not link or PurePosixPath(link).is_absolute() or "\\" in link or "\x00" in link:
                        raise ValueError("Archive contains an unsafe symlink")
                    resolved = posixpath.normpath(str(PurePosixPath(member.name).parent / link))
                    checked_parts(resolved, info["archive_root"])
                    target.symlink_to(link)
                else:
                    raise ValueError("Archive contains a hardlink or unsupported member type")
        # Drain standard tar padding before checking the decompressor's result.
        while process.stdout.read(1024**2):
            pass
        error = process.stderr.read().decode("utf-8", errors="replace")
        if process.wait() != 0:
            raise ValueError("zstd failed: " + error[-1000:].strip())
    finally:
        if process.poll() is None:
            process.terminate()
        process.communicate()
    return staging / info["archive_root"]


def verify_installation(directory: Path, info: dict) -> Path:
    lean = directory / "bin/lean"
    lake = directory / "bin/lake"
    if any(path.is_symlink() or not path.is_file() for path in (lean, lake)):
        raise ValueError("Extracted Lean/Lake executables are missing or unexpected links")
    if not (directory / "lib/lean/Std.olean").is_file():
        raise ValueError("Extracted toolchain is missing its bundled Std library")

    def output(*arguments: str) -> str:
        return subprocess.check_output(arguments, text=True, stderr=subprocess.STDOUT).strip()

    if output(str(lean), "--short-version") != info["version"]:
        raise ValueError("Extracted Lean version differs from the pin")
    if output(str(lean), "--githash") != info["commit"]:
        raise ValueError("Extracted Lean commit differs from the pin")
    version = output(str(lean), "--version")
    if info["target"] not in version:
        raise ValueError("Extracted Lean target differs from the pin")
    if f"Lean version {info['version']}" not in output(str(lake), "--version"):
        raise ValueError("Lake does not use the pinned Lean version")
    print(version, file=sys.stderr)
    return lake.resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, help="use an already downloaded, verified-again archive")
    parser.add_argument("--destination", type=Path, default=ROOT / "build/lean")
    args = parser.parse_args()
    try:
        info = load_manifest()
        if platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"}:
            raise ValueError("This pinned bootstrap supports Linux x86_64 only")
        archive = args.archive.resolve() if args.archive else None
        if archive is not None:
            verify_archive(archive, info)
        destination = args.destination.resolve()
        target = destination / info["archive_root"]
        if target.exists() or target.is_symlink():
            if target.is_symlink() or not target.is_dir():
                raise ValueError("Existing toolchain destination is not a regular directory")
            if json.loads((target / STAMP).read_text(encoding="utf-8")) != info:
                raise ValueError("Existing toolchain provenance differs from the pin")
            print(verify_installation(target, info))
            return 0
        destination.mkdir(parents=True, exist_ok=True)
        if archive is None:
            archive = download_archive(destination / "downloads", info)
        with tempfile.TemporaryDirectory(prefix=".staging-", dir=destination) as temporary:
            extracted = extract_archive(archive, Path(temporary), info)
            verify_installation(extracted, info)
            (extracted / STAMP).write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
            if target.exists() or target.is_symlink():
                raise ValueError("Toolchain destination appeared during extraction; refusing to replace it")
            extracted.rename(target)
        print((target / "bin/lake").resolve())
        return 0
    except (OSError, ValueError, KeyError, TypeError, tarfile.TarError, subprocess.SubprocessError) as error:
        print(f"Lean setup failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
