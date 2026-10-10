import json
import hashlib
from pathlib import Path

root = Path(".")
for manifest_path in root.joinpath("artifacts").rglob("synthetic_processed_manifest_v1.json"):
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    relative_path = manifest.get("provenance_path")
    if not relative_path:
        continue

    file_path = root / relative_path
    expected = manifest.get("provenance_sha256")

    print("\nManifest:", manifest_path)
    print("Provenance path:", relative_path)
    print("Expected SHA256:", expected)

    if file_path.exists():
        actual = hashlib.sha256(file_path.read_bytes()).hexdigest()
        print("Actual SHA256:", actual)
        print("Matches:", actual == expected)
        print("CRLF count:", file_path.read_bytes().count(b"\r\n"))
    else:
        print("Actual SHA256: FILE MISSING")
