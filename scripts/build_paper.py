"""Build the LaTeX manuscript without shell interpolation."""

from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if not shutil.which("latexmk"):
        print("latexmk is missing; see docs/toolchain.md.", file=sys.stderr)
        return 1
    output = ROOT / "build/paper"
    output.mkdir(parents=True, exist_ok=True)
    command = [
        "latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
        "-file-line-error", "-outdir=" + str(output), "main.tex",
    ]
    with (output / "build.log").open("w", encoding="utf-8") as log:
        result = subprocess.run(command, cwd=ROOT / "paper", stdout=log,
                                stderr=subprocess.STDOUT, check=False)
    if result.returncode:
        lines = (output / "build.log").read_text(encoding="utf-8").splitlines()
        print("\n".join(lines[-65:]), file=sys.stderr)
        return result.returncode
    pdf = output / "main.pdf"
    if not pdf.exists():
        print("Build completed without a PDF; inspect build/paper/build.log.",
              file=sys.stderr)
        return 1
    contents = pdf.read_bytes()
    if not contents.startswith(b"%PDF-") or not contents.rstrip().endswith(b"%%EOF"):
        print("The PDF is incomplete; rebuild with make clean && make verify.",
              file=sys.stderr)
        return 1
    print("Built build/paper/main.pdf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
