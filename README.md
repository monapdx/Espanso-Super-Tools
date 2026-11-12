# Espanso Super Tools

<img src="espanso-super-tools.png" alt="Espanso Super Tools: tools for managing triggers and ready-made shortcut collections">

> A collection of scripts, tools, and YAML trigger collections to help you supercharge your use of Espanso.

[![Triggers](https://img.shields.io/badge/%E2%AD%90Triggers-FF2BD6?style=for-the-badge)](https://github.com/monapdx/Espanso-Super-Tools/blob/main/Triggers/Triggers.md) [![Examples](https://img.shields.io/badge/%F0%9F%94%8D%20Examples-FF2BD6?style=for-the-badge&logoColor=000000)](https://github.com/monapdx/Espanso-Super-Tools/blob/main/ways-to-use-espanso.md) [![Download](https://img.shields.io/badge/%E2%AC%87%EF%B8%8F%20Download-FF2BD6?style=for-the-badge)](https://github.com/monapdx/Espanso-Super-Tools/archive/refs/heads/main.zip) 

## What is Espanso?

**[Espanso](https://espanso.org/)** is a text expander that allows you to boost productivity by automating different types of tasks that you create **triggers** for executing.

A trigger is a shortcut you type to make something else happen. For example, you could type `:purple` and have it replaced with your favorite purple's hex code. Or type a shortcut that brings up a form, then have Espanso use your answers to write something for you.

Triggers are stored in simple `.yml` files and can do everything from greatly reducing the amount of typing or data entry required on your part, to running PowerShell scripts, generating code, and much more.

If you're looking for ideas, I've written up some **[ways to use Espanso](ways-to-use-espanso.md)**, with examples you can copy and adapt.

## Find your triggers

After installing Espanso using its [installation instructions](https://espanso.org/install/), navigate to the following folder if you're a Windows user:

```text
C:\Users\USER\AppData\Roaming\espanso\match
```

**USER** is a placeholder that you should replace with your actual Windows username.

There's also a shortcut to get there: press **Win+R**, paste `%APPDATA%\espanso\match`, and press Enter.

Inside that folder, you'll usually find a file called `base.yml`. You can open that in any text editor like Notepad++ and start adding triggers for the tasks you want to speed up and make simpler.

You can also keep different collections in their own `.yml` files in the same folder. If you download a complete collection from here, you can leave it as its own file. If you're copying individual triggers into an existing file, put them beneath its `matches:` line rather than adding another `matches:` line.

## Keep track of your shortcuts

Once you've added a bunch of triggers, remembering all of them can become its own problem.

**[triggers.bat](triggers.bat)** runs **[espanso-shortcuts.py](espanso-shortcuts.py)**, which makes a Markdown file called `espanso-shortcuts.md` in your match folder. It contains a table listing your shortcuts and the files you keep them in, with a blank column where you can write a short description of each one.

### Set it up

1. Click **Code → Download ZIP** on this page and extract the ZIP somewhere convenient, like Downloads. Keep this main folder there; you can add the optional trigger collections to Espanso separately.
2. You'll need Python 3.10 or newer installed, with the `python` command working on your computer.
3. Open the extracted folder in File Explorer, click its address bar, type `cmd`, and press Enter. In the window that opens, paste this command and press Enter:

   ```text
   python -m pip install -r requirements.txt
   ```

   This installs PyYAML, which lets the script read your trigger files.

4. Double-click **`triggers.bat`**. Keep it in the same folder as `espanso-shortcuts.py`. It will look in your usual Windows Espanso match folder, so you don't need to move these two files there.
5. Open `espanso-shortcuts.md` in your match folder and add any descriptions you want in the last column.

After adding or removing triggers, double-click the BAT file again to update your list. **The descriptions you've written stay there when you update it.** New shortcuts get added, and ones you've removed disappear from the list.

If you rename a shortcut or move its file, you'll need to add its description again. A backup of the previous list is saved as `espanso-shortcuts.md.bak` in case you need something from it.

The **[table included here](espanso-shortcuts.md)** shows what the result looks like using the collections in this repo. Yours will list the shortcuts you've actually installed.

## Some triggers to start with

You don't have to start from scratch. Download whichever of these sounds useful:

| Download | What you can do with it |
| --- | --- |
| [HTML elements](Triggers/Triggers.md#html-elements) | Type shortcuts for 102 HTML elements, with the cursor placed where you'll want to start typing |
| [Table generator](Triggers/Triggers.md#table-form) | Type `:mdtable`, fill out a form, and get a table in Markdown along with an HTML version |
| [Custom color names](Triggers/Triggers.md#custom-color-names) | Type `:mycolor` to give a hex code a name you can remember, then use that name whenever you need the code |

The **[trigger instructions](Triggers/Triggers.md)** explain where to put each download and anything else you'll need installed.

## A few things to know about the shortcut list

- If you want to use the `|` character in a description, write it as `\|` so it doesn't split the table into another column. Keep each description on one line.
- If a trigger file has a formatting error, the script will tell you which file needs attention and leave your existing list alone.
- The list includes `.yml` and `.yaml` files inside the folder it reads, including subfolders. It doesn't follow references to files outside that folder or list shortcuts that use pattern matching instead of a fixed trigger. It also doesn't work out which shortcuts are enabled for a particular app.
- If you have an older list that only shows short filenames, descriptions can be carried over when there's only one file with that name. If two files share a name, check your backup for descriptions you need to copy over.

### Using a different folder

If your Espanso files are somewhere else, or you're using macOS or Linux, you can tell the script where to look:

```text
python espanso-shortcuts.py --match-dir "PATH/TO/espanso/match"
```

Replace `PATH/TO/espanso/match` with your actual folder. On some computers, the command is `python3` instead of `python`.

### If you're helping work on the tools

After installing the requirements, run `python -m unittest discover -s tests -v` to check the shortcut script and included YAML files. The Windows forms and PowerShell output still need to be tried in Espanso itself.
