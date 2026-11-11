# Optional trigger packs

Install only what you want. On standard Windows installations, open `%APPDATA%\espanso\match`. For a `.yml` pack, download the raw file rather than saving the GitHub HTML page, and place it inside that folder. Restart Espanso if it does not reload automatically.

## Table form

Download [table-generator.yml](https://raw.githubusercontent.com/monapdx/Espanso-Super-Tools/main/Triggers/table-generator.yml) into your match folder. Requires Windows PowerShell.

Type **`:mdtable`** to open a form with two dropdown selections, a title, and multiline content. It outputs a fixed field/value Markdown table, a content block, and a complete styled HTML document inside a code fence. It does not ask for arbitrary row/column counts. Customize dropdown options and labels in the YAML.

The HTML is source text: copy the document out of the code fence into an `.html` file to view it. Form values are HTML-encoded. Markdown table fields escape pipes and line breaks, and content fences adapt to embedded backticks.

The HTML element pack separately uses **`:table`** for `<table></table>`; the names intentionally differ. If you previously installed the form as `:table`, replace that old definition rather than keeping both.

## HTML elements

Download [html.yml](https://raw.githubusercontent.com/monapdx/Espanso-Super-Tools/main/Triggers/html.yml) into your match folder.

Includes 102 HTML element snippets. Type a trigger followed by Space: for example, `:article` inserts `<article></article>` and places the cursor inside. `$|$` in the YAML marks the cursor position. Void elements such as `<img>` have no closing tag.

Some triggers use memorable aliases: `:para` → `<p>`, `:url` → `<a>`, `:row` → `<tr>`, and `:cell` → `<td>`. Edit or remove triggers that conflict with your own collection. This is a broad collection, not every HTML element.

## Custom color names

Download [espanso-mycolor.zip](https://raw.githubusercontent.com/monapdx/Espanso-Super-Tools/main/Triggers/espanso-mycolor.zip) into your match folder and extract it there. Open the extracted folder and run **`setup-windows.bat`** once, then restart Espanso. Requires Python 3.10+ with tkinter; setup installs PyYAML and configures the actual extracted script path. Extra extraction folders are supported.

Type **`:mycolor`**, enter a name such as `brandpink` and a hex code such as `#e69dfc`, then select:

- **Save to my colors:** adds the trigger to `match/mycolors.yml`. Typing `:brandpink` then inserts `#e69dfc`. Updating an existing color asks for confirmation.
- **Generate YAML only:** inserts YAML in the active editor without saving a match file. When merging into an existing file, copy only the match list entry beneath `matches:`.

These are separate files: the bundled **`mycolor.yml` defines the form**; **`mycolors.yml` stores your created colors** and is created on the first save. There is no need to ship an empty palette.

Remove older `:mycolor` definitions and older extracted package folders before installing. Keep existing color data. If migrating from `my-colors.yml`, back it up and rename it to `mycolors.yml` only if the destination does not exist; merge manually if both files exist. Duplicate triggers in other YAML files are blocked during saving.

Run setup again after moving the extracted folder. The package README contains backup, validation, removal, and troubleshooting details. Remove the extracted package to uninstall the form; your saved colors remain independently usable.
