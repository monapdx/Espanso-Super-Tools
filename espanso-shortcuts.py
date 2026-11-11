"""Create a Markdown index beside this script in the Espanso match folder."""

import os
import re
import shutil
from pathlib import Path


match_dir = Path(__file__).resolve().parent
output = match_dir / "espanso-shortcuts.md"
pattern = re.compile(r'^\s*-?\s*trigger:\s*[\'\"]?([^\'\"\s#]+)')

if not match_dir.is_dir():
    raise SystemExit(f"Espanso match folder not found: {match_dir}")

rows = []
for path in sorted(match_dir.rglob("*")):
    if path.suffix.lower() not in {".yml", ".yaml"}:
        continue
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        found = pattern.match(line)
        if found:
            rows.append((found.group(1), path.stem))

rows.sort(key=lambda row: (row[0].lower(), row[1].lower()))

# Read descriptions before regenerating the table. Match both columns so
# identical triggers in different match files keep their own descriptions.
descriptions = {}
if output.exists():
    headers = None
    for line in output.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
        if "Trigger" in cells and "File" in cells:
            headers = cells
            continue
        if headers is None or "Description" not in headers or len(cells) != len(headers):
            continue
        trigger = cells[headers.index("Trigger")].strip("`")
        filename = cells[headers.index("File")]
        descriptions[(trigger, filename)] = cells[headers.index("Description")]

lines = [
    "# Espanso Shortcuts",
    "",
    f"**{len(rows)} shortcuts**",
    "",
    "| Trigger | File | Description |",
    "| --- | --- | --- |",
]
lines.extend(
    f"| `{trigger}` | {filename} | {descriptions.get((trigger, filename), '')} |"
    for trigger, filename in rows
)
# Keep the previous table as a backup and replace only after writing succeeds.
temporary = output.with_suffix(".md.tmp")
temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
if output.exists():
    shutil.copy2(output, output.with_suffix(".md.bak"))
temporary.replace(output)
print(f"Saved {len(rows)} shortcuts to {output}")
