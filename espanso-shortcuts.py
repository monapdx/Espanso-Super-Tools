"""Index actual Espanso YAML matches while preserving editable descriptions."""
import argparse
import html
import re
import shutil
from collections import Counter
from pathlib import Path
import yaml


def cell(value):
    return html.escape(str(value), quote=False).replace('|', '&#124;').replace('\r', '').replace('\n', '<br>')


def read_descriptions(output, rows):
    descriptions = {}
    # Legacy indexes used stems; migrate only when the stem identifies one file.
    stems = {}
    for _, filename in rows:
        stems.setdefault(Path(filename).stem, set()).add(filename)
    if not output.exists():
        return descriptions
    headers = None
    for line in output.read_text(encoding='utf-8-sig').splitlines():
        if not line.strip().startswith('|'):
            continue
        cells = [c.strip() for c in re.split(r'(?<!\\)\|', line.strip())[1:-1]]
        if all(h in cells for h in ('Trigger', 'File', 'Description')):
            headers = cells
            continue
        if headers is None or len(cells) != len(headers):
            continue
        trigger = html.unescape(cells[headers.index('Trigger')].removeprefix('<code>').removesuffix('</code>').strip('`'))
        filename = html.unescape(cells[headers.index('File')])
        description = cells[headers.index('Description')]
        if filename in stems and len(stems[filename]) == 1:
            filename = next(iter(stems[filename]))
        descriptions[(trigger, filename)] = description
    return descriptions


def collect(folder):
    rows = []
    for path in sorted(folder.rglob('*')):
        if path.suffix.lower() not in {'.yml', '.yaml'}:
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding='utf-8-sig'))
            if data is None:
                continue
            if not isinstance(data, dict):
                raise ValueError('expected a YAML mapping')
            matches = data.get('matches', [])
            if not isinstance(matches, list):
                raise ValueError('matches must be a list')
            for match in matches:
                if not isinstance(match, dict):
                    raise ValueError('each match must be a mapping')
                triggers = match.get('triggers', [])
                if not isinstance(triggers, list):
                    raise ValueError('triggers must be a list')
                triggers = list(triggers)
                if 'trigger' in match:
                    triggers.append(match['trigger'])
                if any(not isinstance(t, str) for t in triggers):
                    raise ValueError('triggers must be strings')
                rows.extend((t, path.relative_to(folder).as_posix()) for t in dict.fromkeys(triggers))
        except (ValueError, yaml.YAMLError, UnicodeError, OSError) as error:
            raise ValueError(f'{path}: {error}') from error
    return sorted(rows, key=lambda row: (row[0].lower(), row[1].lower()))


def generate(folder, output):
    folder = Path(folder).resolve()
    output = Path(output).resolve()
    if not folder.is_dir():
        raise ValueError(f'Match folder not found: {folder}')
    rows = collect(folder)  # Complete validation before touching existing output.
    descriptions = read_descriptions(output, rows)
    lines = ['# Espanso Shortcuts', '', f'**{len(rows)} shortcuts**', '',
             '| Trigger | File | Description |', '| --- | --- | --- |']
    lines.extend(f'| <code>{cell(t)}</code> | {cell(f)} | {descriptions.get((t, f), "")} |' for t, f in rows)
    temporary = output.with_suffix('.md.tmp')
    temporary.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    if output.exists():
        shutil.copy2(output, output.with_suffix('.md.bak'))
    temporary.replace(output)
    for trigger, count in Counter(t for t, _ in rows).items():
        if count > 1:
            print(f'Note: {trigger} appears {count} times; check whether these are intentional app-specific matches.')
    return len(rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--match-dir', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        destination = args.output or args.match_dir / 'espanso-shortcuts.md'
        count = generate(args.match_dir, destination)
        print(f'Saved {count} shortcuts to {destination}')
    except (ValueError, OSError) as error:
        parser.exit(1, f'Index not updated: {error}\n')
