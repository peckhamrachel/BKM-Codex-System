# Ren'Py Codex System

A plug-and-play in-game encyclopedia system for projects made in Ren'Py. Lets players browse unlockable lore entries organized by category, and allows writers to embed clickable inline links directly into dialogue.

---

## Features

- **Inline dialogue links** — embed clickable hyperlinks directly in speech that open the relevant codex entry
- **Unlock tracking** — entries stay hidden until your project unlocks them
- **Dynamic categories** — define as many categories as you need; the menu screen organizes itself automatically
- **Seen/unseen state** — entries are visually flagged as new until the player views them
- **Versioned persistence** — safe to update mid-playthrough without breaking existing saves
- **Customizable colors** — all colors defined as constants at the top of the file

---

## Installation

First, place the `codex.rpy` file into your game's `/game` folder.

Then, add the following to the `screen navigation():` block in your `screens.rpy` file:

```renpy
textbutton _("Codex") action ShowMenu("codex")
```

You must do this to add the Codex button to your pause menu.

---

## Setup

### 1. Define your categories and entries

In `codex.rpy`, find the `create_persistent_game_data()` function and replace the example dictionaries with your own. For example, you could write something like:

```renpy
"charactersDict": {
    "Evelyn": {
        "unlocked": False,
        "button_name": "Evelyn Cross",
        "seen": False
    },
    "Marcus": {
        "unlocked": False,
        "button_name": "Marcus Vane",
        "seen": False
    }
},
"locationsDict": {
    "TheTower": {
        "unlocked": False,
        "button_name": "The Tower",
        "seen": False
    }
}
```

To properly work, each entry must have the following three fields:
- `unlocked` — whether the entry is visible to the player (`False` to start)
- `button_name` — the display name shown on the button
- `seen` — whether the player has viewed it since it was last updated (`False` to start)

### 2. Write your entry content

In the `screen codexEntry(kw):` block, add a branch for each entry keyword. For example, to match the previous example:

```renpy
if kw == "Evelyn":
    text "Evelyn Cross. Researcher. Probably knows more than she's saying."

elif kw == "TheTower":
    text "A structure that shouldn't exist. No one agrees on when it appeared."
```

Keywords must match the name of the corresponding entry in order to work properly.

### 3. Customize the appearance (optional)

At the top of `codex.rpy`, adjust the color constants to match your game's visual style as you wish. For example:

```renpy
define button_color = "#28962d"
define button_hover_color = "#238528"
define button_seen_color = "#539256"
define button_seen_hover_color = "#5e8460"
define button_inactive_color = "#a69c8f"

define frame_border_color = "#28962d"
define frame_body_color = "#0e0e0e"
```

---

## Usage

### Unlocking an entry

Call `updateCodex` with the entry keyword, the field to update, and the new value, like this:

```renpy
call updateCodex("Evelyn", "unlocked", True)
```

This can go anywhere in your script — at a story beat, after a conversation, when a flag is set. Put it where it feels right.

### Inline dialogue links

Embed a clickable link directly in a line of dialogue using this syntax:

```renpy
"{a=codex:findCodex|Evelyn}Evelyn{/a} didn't look up when I entered the room."
```

The player can click the highlighted word to open the codex entry in the pause menu, and their point in the story will be saved when they return.

> **Note:** Inline links don't unlock entries on their own. Remember to call `updateCodex` first to unlock the entry, then use the inline link so the player can access it.

---

## How it works

Entries are stored in `persistent.game_data`, organized by category dictionary. The `updateCodex` label iterates over all category dictionaries dynamically, so adding new categories requires no changes to the core logic — just add a new dictionary to `create_persistent_game_data()` and populate your entries.

The versioning system checks `persistent.game_data["version"]` on launch. If a player's saved version is older than the current one, the data structure is refreshed. You can use this to safely add new entries in updates without breaking existing saves; simply change the version number as you see fit.

---

## Built with this system

[Libera Me!](https://beetlemachine.itch.io/libera-me) — a dark comedy visual novel set in hell

---

## License

MIT License — free to use in personal and commercial projects. Credit appreciated but not required.
