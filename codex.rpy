# IMPORTANT: 
# Make sure the following is in your screens.rpy file among the other textbuttons found in screen navigation():
#
# textbutton _("Codex") action ShowMenu("codex")
#
# Otherwise, the codex option won't appear in your pause menu.

init:
    # define constant variables
    define small_button_x = 320
    define small_button_y = 50

    define large_button_x = 425
    define large_button_y = 100

    define button_color = "#28962d"
    define button_hover_color = "#238528"
    define button_seen_color = "#539256"
    define button_seen_hover_color = "#5e8460"
    define button_inactive_color = "#a69c8f"

    define frame_border_color = "#28962d"
    define frame_body_color = "#0e0e0e"

# hyperlink behavior
init python: 

    def handle_hyperlink(data):
        args = data.split('|')
        label_name = args.pop(0)
        keyword_name = args.pop(0)
        renpy.call_in_new_context(label_name, keyword_name)

    config.hyperlink_handlers['codex'] = handle_hyperlink

# define game_data structure
default persistent.game_data = {
    "version": 0
}

# populate game_data structure
init python:
    def create_persistent_game_data():
        persistent.game_data = {
            # define dictionaries
            "version": 1,
            "exampleDict1": {
                "Information": {
                    "unlocked": False,
                    "button_name": "One",
                    "seen": False
                },
                "moreInformation": {
                    "unlocked": False,
                    "button_name": "Two",
                    "seen": False
                }
            }, # <- remember comma between dictionaries
            "exampleDict2": {
                "otherInformation": {
                    "unlocked": False,
                    "button_name": "One",
                    "seen": False
                },
                "furtherInformation": {
                    "unlocked": False,
                    "button_name": "Two",
                    "seen": False
                }
            }

            #
            # and so on
            #

        }

# Take the given keyword and pass it to the codex menu screen for viewing.
label findCodex(keyword):

    # Set up scene.
    show black

    # Ensure keyword is a string.
    if not isinstance(keyword, str):
        $ kw = keyword[0]
    else:
        $ kw = keyword
    
    call updateCodex(kw, "seen", True)
    call screen codexEntry(kw)

    # Clean up scene before leaving.
    nvl clear
    hide black
    if main_menu:
        $ renpy.full_restart()
    return

# Update the values for the given keyword.
label updateCodex(keyword, field, value):
    $ data = None
    $ categories = {k: v for k, v in persistent.game_data.items() if isinstance(v, dict)}
    
    python:
        for cat_name, cat_dict in categories.items():
            if keyword in cat_dict:
                data = cat_dict[keyword]
                break
    
        if data is not None:
            # Update specified field.
            data[field] = value
            # If not updating the seen field...
            if not field == "seen":
                # flag updated entry as unseen.
                data["seen"] = False
    
    return


# Codex menu screen setup
# Screen changes contents depending on the selected keyword's values.

screen codexEntry(kw):
    tag menu
    use game_menu(_("Codex"), scroll="viewport"):

        frame:
            background frame_border_color
            padding (4, 4)
            margin (0, 0)

            frame: 
                background frame_body_color
                padding (20, 20)
                xfill True

                vbox:
                    if kw == "Information":
                        text "Sample Text 1"

                    elif kw == "moreInformation":
                        text "Sample Text 2"
                    
                    elif kw == "otherInformation":
                        text "Sample Text 3"

                    #
                    # and so on
                    #
 
        text " "

        button:
            background button_color
            hover_background button_hover_color
            text "Back"
            action Show("codex")

# Example menu screen setup
# Setting up a screen for each dictionary is advised to allow the player to access entries with ease.

screen codex():
    tag menu
    use game_menu(_("Codex"), scroll="viewport"):

        frame:
            background frame_border_color
            padding (10, 10)
            margin (0, 0)
            xalign 0.5
            yalign 0.5

            vbox:
                spacing 20

                text "{size=25}Placeholder Codex Title{/size}"

        text " "
        
        $ categories = {k: v for k, v in persistent.game_data.items() if isinstance(v, dict)}
        for cat_name in categories:
            $ cat_dict = categories[cat_name]
            $ num_entries = len(cat_dict)
            $ charRow = num_entries // 3 + (1 if num_entries % 3 != 0 else 0)

            text cat_name

            # construct button grid based off number of entries in array.
            grid 3 charRow: 
                style_prefix "slot"
                xalign 0.5
                yalign 0.5
                spacing gui.slot_spacing

                for name in cat_dict:
                    $ info = cat_dict[name]
                    # if unlock is set to True...
                    if info["unlocked"]:
                        # construct button with name.
                        button:
                            xysize (large_button_x, large_button_y)
                            # check if entry has been seen since last updated
                            if not info["seen"]:
                                background button_color
                                hover_background button_hover_color
                            else:
                                background button_seen_color
                                hover_background button_seen_hover_color

                            text [info["button_name"]]
                            action Call("findCodex", keyword=name)
                    # otherwise, construct fake button.
                    else:
                        button:
                            xysize (large_button_x, large_button_y)
                            background button_inactive_color
                            text "???"

# populate codex on first launch
label before_main_menu:
    if persistent.game_data.get("version", -1) < 1:
        $ create_persistent_game_data()
    return 

label start:
    jump exampleStory

label exampleStory:
    # Calling updateCodex 
    # Format: call updateCodex("entryName", "field", value)
    # Call this function to change the contents of a codex entry.
    
    call updateCodex("moreInformation", "unlocked", True)

    # Inline Labels 
    # Format: {a=codex:findCodex|entryName}text{/a}
    # Use this inline label to provide a link for readers to click on to access the corresponding codex entry.

    "You can find more information by clicking on this {a=codex:findCodex|moreInformation}inline label{/a}. Make use of it!"

    # Note: the inline label cannot unlock a codex entry on its own. Use in tandem with updateCodex for best effect.
