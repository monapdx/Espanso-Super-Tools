"""Personal color vocabulary for Espanso 2. Requires PyYAML and tkinter."""
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path


def normalize(name, value):
    name = name.strip().removeprefix(':')
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,63}', name):
        raise ValueError('Use a name starting with a letter, followed by letters, numbers, _ or - (64 characters maximum).')
    if name == 'mycolor':
        raise ValueError(':mycolor is reserved for the color form.')
    value = value.strip().removeprefix('#')
    if not re.fullmatch(r'(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})', value):
        raise ValueError('Enter a CSS hex color with 3, 4, 6 or 8 digits, with or without #.')
    return ':' + name, '#' + value.lower()


def load(path, require_matches=True):
    import yaml
    if not path.exists():
        return {'matches': []}
    data = yaml.safe_load(path.read_text(encoding='utf-8-sig'))
    if not require_matches and (data is None or isinstance(data, dict) and 'matches' not in data):
        return {'matches': []}
    if not isinstance(data, dict) or not isinstance(data.get('matches'), list):
        raise ValueError(f'Expected a matches list in {path}. No files were changed.')
    if any(not isinstance(item, dict) for item in data['matches']):
        raise ValueError(f'Invalid match entry in {path}. No files were changed.')
    return data


def has_trigger(item, trigger):
    return item.get('trigger') == trigger or trigger in (item.get('triggers') or [])


def save_color(config, trigger, value, confirm):
    import yaml
    folder = Path(config) / 'match'
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / 'my-colors.yml'
    # Exclusive lock prevents two helper processes from losing each other's changes.
    lock = folder / '.mycolor.lock'
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise ValueError('Another color save is running. Try again. If a previous save crashed, remove match/.mycolor.lock.')
    os.close(fd)
    temp = None
    try:
        before = target.read_bytes() if target.exists() else None
        data = load(target)
        for path in sorted(folder.rglob('*')):
            if path.suffix.lower() not in ('.yml', '.yaml') or path == target:
                continue
            other = load(path, require_matches=False)  # Fail closed if conflict checking cannot read a file.
            if any(has_trigger(item, trigger) for item in other['matches']):
                raise ValueError(f'{trigger} already exists in {path.name}. Choose another name or edit that file.')
        existing = [item for item in data['matches'] if has_trigger(item, trigger)]
        if len(existing) > 1:
            raise ValueError(f'Multiple entries for {trigger} exist in my-colors.yml. Resolve them manually first.')
        if existing:
            old = existing[0]
            if set(old) != {'trigger', 'replace'} or not isinstance(old['replace'], str):
                raise ValueError('This name belongs to a complex match. Choose another name or edit it manually.')
            if old['replace'] == value:
                return 'unchanged'
            if not confirm(trigger, old['replace'], value):
                return 'cancelled'
            old['replace'] = value
        else:
            data['matches'].append({'trigger': trigger, 'replace': value})
        text = '# Personal colors managed by :mycolor. Keep custom comments in a separate file.\n'
        text += yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='\n', prefix='.mycolor-', suffix='.tmp', dir=folder, delete=False) as stream:
            temp = Path(stream.name)
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        if (target.read_bytes() if target.exists() else None) != before:
            raise ValueError('The color file changed during this save. Please try again.')
        if before is not None:
            shutil.copy2(target, folder / 'my-colors.yml.bak')
        os.replace(temp, target)
        return 'saved'
    finally:
        if temp and temp.exists():
            temp.unlink()
        lock.unlink()


def main():
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    try:
        import yaml
        trigger, value = normalize(os.environ.get('ESPANSO_COLOR_NAME', ''), os.environ.get('ESPANSO_COLOR_HEX', ''))
        action = os.environ.get('ESPANSO_COLOR_ACTION', '')
        if action == 'Generate YAML only':
            sys.stdout.write(yaml.safe_dump({'matches': [{'trigger': trigger, 'replace': value}]}, sort_keys=False))
            return
        if action != 'Save to my colors':
            raise ValueError('Choose Save to my colors or Generate YAML only.')
        config = os.environ.get('CONFIG')
        if not config:
            raise ValueError('Espanso did not supply CONFIG. Run this helper through :mycolor.')
        result = save_color(config, trigger, value, lambda name, old, new: messagebox.askyesno('Update personal color?', f'{name}\nCurrent: {old}\nNew: {new}\n\nReplace this color?', parent=root))
        if result != 'cancelled':
            messagebox.showinfo('Personal color', f'{trigger} = {value}\n\n' + ('Already saved.' if result == 'unchanged' else 'Saved to my-colors.yml. Espanso should reload it automatically.'), parent=root)
        # Save mode inserts no status text into the active document.
    except Exception as error:
        messagebox.showerror('Color could not be created', str(error), parent=root)
    finally:
        root.destroy()


if __name__ == '__main__':
    main()

