Espanso is much more than a text expander. I've found countless uses for it since installing and setting up my first few triggers. You can create convenient shorthands for entire markup languages, or even use it as a snippet manager for scripts and bits of code you run all the time.

## HTML Elements

You can create an Espanso trigger for each of the 100+ HTML elements that exist.

A few need some modifications due to the way Espanso works.

Most can just use the tag as the trigger.

So for example:

`:article = <article></article>`

`:section = <section></section>`

A few are worth giving a longer name. For example, if you make the trigger `:b` and it replaces the text as soon as you type it, you won't get a chance to finish typing another shortcut that starts with `:b`.

You can use a name like `:bold` instead. Or add `word: true`, like in the example below, so Espanso waits until you press Space before replacing it. The HTML collection uses that setting.

For the paragraph tag, I used `:para` instead of just `:p`.

Here is how the actual triggers would be setup as YAML:

```
  - trigger: ":blockquote"
    word: true
    replace: "<blockquote>$|$</blockquote>"
```



## HEX Color Codes

You can develop natural color name triggers to correspond to your favorite and most often used HEX color codes.

For example, I have my favorite handful setup as triggers like the following:

`:purple = #e69dfc`

`:green = #39ff14`

`:pink = #ff00b3`

Here is how the actual trigger would be setup as YAML:

```
  - trigger: ":purple"
    replace: "#e69dfc"
```

If you want to set up your own color vocabulary using Espanso, download **[espanso-mycolor.zip](https://raw.githubusercontent.com/monapdx/Espanso-Super-Tools/main/Triggers/espanso-mycolor.zip)** into your Espanso match folder and extract it there. Run `setup-windows.bat` inside the extracted folder once, then restart Espanso. You'll need Python 3.10 or newer, with tkinter (included in the normal Windows Python installation). Setup installs the extra Python tool it needs, PyYAML, and makes sure it can find the script.

That will make a form pop up when you type `:mycolor`, asking for the hex code and the name you want to use for it. Then when you submit it, it will write the trigger and add it to a file called `mycolors.yml`. You can also choose to have it write out the YAML for you to copy and paste yourself.

**`mycolor.yml` is the form trigger. `mycolors.yml` is your collection of color triggers.** The [setup instructions](Triggers/Triggers.md#custom-color-names) explain it step by step.

Never copy and paste another color code when writing CSS again. You're welcome.

## Contact Emails

You might have some people you communicate with via email that have used *a lot* of different email addresses over the years. 

I have a couple offenders in my contact's list for sure. 

If you want to search for emails from all of them to get every email they've sent you, you can set up a trigger that uses their name and then inserts all of their different email addresses, to quickly search your Gmail inbox for every email they've sent you from each one.

This trigger ends up creating the following reality:

Contact first name = every email address that belongs to them

Here's how the trigger would be setup as YAML:

```
  - trigger: ":name"
    replace: '{from:email@yahoo.com from:email@gmail.com from:email@aol.com  from:email@comcast.net}'
```

## Use it to Explore Data Exports

Say you exported your search history from Google. You can upload your JSON or CSV files to OpenRefine and then choose query column and create a custom text facet.

Maybe you want to find all your searches that contain the word "free"

You'd paste something like this:

`if(value.toLowercase().contains("free"), "free", "Other searches")`

You can setup an Espanso trigger using whatever you want to automatically paste the structure of that filtering action, returning the cursor to between the quotes so you can  just start typing the word you want to filter by.

Here is how the actual trigger would be setup as YAML:

```
 - trigger: ":refine"
   replace: 'if(value.toLowercase().contains("$|$"), "Matches", "Other searches")'
```


## Project or Template Scaffolding

Say you have a file template that you use often, or you create the same type of project with considerable frequency.

This might be anything from an HTML page template you reuse a lot, to creating lots of apps using React.

Here is one I use to make the  manifest.json file for a new Obsidian plugin I'm making:

```
  - trigger: ":obsidian"
    replace: |
      {
        "id": "$|$",
        "name": "",
        "version": "1.0.0",
        "minAppVersion": "1.4.0",
        "description": "",
        "author": "Ashly Lorenzana",
        "isDesktopOnly": false
      }
```

## Chrome's Dev Tools

You can use Espanso triggers to save bits of javascript that you can paste into the dev tools console in Google Chrome.

These can do everything from list all the links on a webpage, to extracting all of the div classes. 

To open dev tools on any page, open it in Chrome and hit F12. Click on the Console tab, then paste your javascript and hit enter to run it.

For example, here is one of my triggers that outlines every element on the page, so you can see the layout clearly:

```
  - trigger: ":outline"
    replace: |
      document.querySelectorAll("*").forEach(el => {
        el.style.outline = "1px solid magenta";
      }); 
```













