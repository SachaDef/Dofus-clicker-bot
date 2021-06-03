# Dofus-clicker-bot

Click-based bot for the french videogame Dofus, useful for automated deplacement (and soon automated resource farming).
Clearly not ready yet, fixes and functionalities yet to be implemented.


## Current state of the project
---

### What is implemented
- The traveling bot with various features such as :
    - pop-up windows to show current position
    - auto-traveling enabled even when watching another window/working on another screen, the bot manages the windows switching

### What is yet to be implemented
- The farming bot
- A bugfix with tkinter not looping in main thread
- A portable program ? It probably only works on my computer for now, given that I gave him precise pixel coordinates for mouse events, that it is based on Windows, ...


## Organization of the project
---

- [`img`](img) folder containing icons and images for the GUI (duh) &rarr; implemented 
- [`main_bot`](main_bot/) folder containing the two python file describing the `DofusBot` class and its GUI, in [`main_bot.py`](main_bot/main_bot.py) and [`main_gui.py`](main_bot/main_gui.py) respectively &rarr; implemented, bug with tkinter not looping in main thread to be fixed
- [`maps_paths`](maps_paths/) folder containing two databases and their [`db_manager.py`](maps_paths/db_manager.py), to store coordinates of resources and interesting paths for farming in [`maps.db`](maps_paths/maps.db) and [`paths.db`](maps_paths/paths.db) respectively &rarr; not implemented
- [`utilities`](utilities) folder containing :
    - [`message_boxes.py`](utilities/message_boxxes.py), graphical helper providing a confirmation pop-up window and a self-destroying pop-up window &rarr; implemented
- [`.gitignore`](.gitignore) file
- [`main_commands.txt`](main_commands.txt) file listing the keys and their interaction upon the bot and/or the GUI
- [`main.py`](main.py) file creating the bot, listening to keyboard and mouse events, managing the bot in general &rarr; partially implemented


## How it works
---

(See [`main.py`](main.py))
1. First, your Dofus window must be opened when you launch the [`main.py`](main.py) otherwise it won't be able to detect it.
2. A window then pops-up asking for you character x and y location, described in the [`main_gui.py`](main_bot/main_gui.py). Once you filled the fields, hit enter to send those coordinates to the `DofusBot` object.
3. A keyboard listener is then launched from [`main.py`](main.py), with various inputs listed, all available in the [`main_commands.txt`](main_commands.txt). Depending on the input and desired action, either a simple click to change maps is done if the Dofus window is active, either a thread is launched to manage a sleep-click cycle with windows switching to automate traveling, or all threads are terminated and all actions interrupted. A special key is reserved to completely kill the bot and end the program.
