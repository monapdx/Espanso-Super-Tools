# Triggers

Here are some collections you can add to Espanso to start doing useful things without writing all the triggers yourself.

On Windows, press **Win+R**, paste `%APPDATA%\espanso\match`, and press Enter to open your match folder.

The download links below open the actual files. For a `.yml` file, save that file in your match folder, keeping the `.yml` extension. Restart Espanso if your new shortcuts don't start working automatically.

## Table form

**[Download table-generator.yml](https://raw.githubusercontent.com/monapdx/Espanso-Super-Tools/main/Triggers/table-generator.yml)**

Type **`:mdtable`** to bring up a form with two dropdowns, a title, and a space for whatever content you want to include. Fill it out, submit it, and it will write a table in Markdown, followed by an HTML version of the same information.

This one uses a set layout: a Field column and a Value column. You can open the YAML file in your text editor to change the dropdown options and labels to whatever makes sense for you. It needs Windows PowerShell to make the HTML version.

The HTML version includes the code for a whole webpage. Copy everything from `<!doctype html>` through `</html>` into a new file, save it with an `.html` extension, and open it in your browser to see the result. Leave out the lines of tildes (`~~~`) that surround the code in the output.

## HTML elements

**[Download html.yml](https://raw.githubusercontent.com/monapdx/Espanso-Super-Tools/main/Triggers/html.yml)**

`html.yml` is a collection of triggers that correspond to HTML elements. It contains 102 of them, and you can add or remove whatever ones you don't need or that conflict with other triggers you use.

Type a trigger and then press Space. For example, `:article` becomes `<article></article>`, with your cursor between the tags so you can start typing right away.

Some use slightly different names: `:para` inserts a paragraph, `:url` inserts a link, `:row` inserts a table row, and `:cell` inserts a table cell.

If you're editing the file yourself, `$|$` marks where the cursor will go. Elements like `<img>` don't need a closing tag, so those shortcuts only insert the opening one.

## Custom color names

**[Download espanso-mycolor.zip](https://raw.githubusercontent.com/monapdx/Espanso-Super-Tools/main/Triggers/espanso-mycolor.zip)**

You can develop your own color vocabulary, using names you actually remember instead of looking up hex codes every time you need them.

1. Save the ZIP in your match folder and extract it there.
2. Open the extracted folder and double-click **`setup-windows.bat`**. You'll need Python 3.10 or newer installed. The normal Windows Python installer includes tkinter, which is what the helper uses to show its messages. Setup installs PyYAML and tells the trigger where to find the script, even if extracting the ZIP created an extra folder.
3. Restart Espanso, then type **`:mycolor`**.

The form asks for a hex code and the name you want to use for it. For example, enter `brandpink` and `#e69dfc`. Choose **Save to my colors**, submit it, and now typing `:brandpink` will insert `#e69dfc`.

If you'd rather add the trigger to a file yourself, choose **Generate YAML only**. It will write the YAML into whatever editor you're using. When adding it to a file that already has a `matches:` line, copy just the trigger underneath that line, rather than adding a second one.

**`mycolor.yml` is the trigger that brings up the form. `mycolors.yml` is the separate file where it stores the color triggers you add.** The second file gets created when you save your first color.

Use the same name again if you want to change its color. It will show you the old code and ask before replacing it. If that name is already used by a trigger in another YAML file, it will ask you to choose a different name instead.

## Markdown

**[Download markdown.yml](https://github.com/monapdx/Espanso-Super-Tools/blob/main/Triggers/markdown.yml)**

`markdown.yml` is a collection of triggers that make it much faster to use markdown conventions. 

It includes triggers to create code blocks (even nested ones that contain markdown themselves), inline code, bold links, etc. 

## Obsidian

**[Download obsidian.yml](https://github.com/monapdx/Espanso-Super-Tools/blob/main/Triggers/obsidian.yml)**

`obsidian.yml` is a collection of triggers for use with the popular note taking software Obsidian. 

It has triggers for automatically adding frontmatter to notes depending on the type of content, and even a form that will help you generate a manifest.js file for creating an Obsidian plugin.
