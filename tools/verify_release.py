"""Fast, dependency-free release checks for public publication."""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IPV4 = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])")
FORBIDDEN = ("C:\\Users", "/home/matthew", "api" + "_key", "authorization: bearer")


def main():
    bad = []
    digests = {}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = path.relative_to(ROOT).as_posix()
        content = path.read_bytes()
        digests[relative] = {"sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)}
        public_text = relative.startswith(("data/", "evaluation/", "docs/", "site/")) or path.name in {"README.md", "CHANGELOG.md", "CITATION.cff"}
        if public_text and path.suffix in {".jsonl", ".md", ".yaml", ".yml", ".html", ".js", ".txt", ".cff"}:
            text = content.decode("utf-8", errors="replace")
            if IPV4.search(text) or any(token.lower() in text.lower() for token in FORBIDDEN):
                bad.append(relative)
    if bad:
        print("public-safety check failed: " + ", ".join(bad), file=sys.stderr)
        return 1
    manifest = {"release": "tpot-evidence-lab-v3", "files": digests}
    (ROOT / "release-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"verified {len(digests)} files; wrote release-manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

