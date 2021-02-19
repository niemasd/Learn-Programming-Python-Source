This repository contains the source code of the game engine behind [Learn Programming: Python](https://store.steampowered.com/app/1536770/Learn_Programming_Python/). The two key files are [`game.py`](game.py) (the main source of the game) and [`universal.py`](universal.py) (a helper file).

If you have already purchased the game, you can simply drop these files into the game installation directory, and they should be able to load the lesson data just fine. To locate the game's installation directory, you can do the following:

1. Open Steam
2. Click on the "Learn Programming: Python" game in your Steam library
3. Click on the gear button at the top-right of the page (directly under the game banner)
4. Highlight the "Manage" menu, and click "Browse local files"
5. The folder that Steam opens is the game's installation directory
    * You can drop `game.py` and `universal.py` in this folder, and then you can simply double-click `game.py` to play!

Enjoy :-)

# Running on Non-Windows OS
This open source game engine should work on any platform (not just Windows). To run it on non-Windows operating systems, you can do the following (instructions adapted from [Knee Scabs](https://steamcommunity.com/id/Knee_Scabs); thank you!):

## Step 1: Download Source to Steam Game Installation Directory
1. Open Steam
2. Click on the "Learn Programming: Python" game in your Steam library
3. Click on the gear button at the top-right of the page (directly under the game banner)
4. Highlight the "Manage" menu, and click "Browse local files"
5. The folder that Steam opens is the game's installation directory
6. Download [`game.py`](game.py) and [`universal.py`](universal.py) to the folder that was opened

## Step 2: Editing the Source Code to Remove Windows Dependencies
1. Comment out (`#`) [line 220 of `game.py`](game.py#L220)
2. On [line 22 of `universal.py`](universal.py#L22), replace `ALT+ENTER` with `F11`
3. Comment out (`#`) [lines 108-138 of `universal.py`](universal.py#L108-L138)
    * `msvcrt` is a Windows-only module and is invoked by this in the start up

## Step 3: Install [`prompt_toolkit`](https://python-prompt-toolkit.readthedocs.io/en/master/pages/getting_started.html#installation)
* If you have `pip` installed, you would install `prompt_toolkit` from the command line like this: `pip install prompt_toolkit`
* If you *don't* have `pip` installed, you might be able to just download this [`prompt_toolkit`](https://github.com/prompt-toolkit/python-prompt-toolkit/tree/master/prompt_toolkit) folder and also add it to the game's installation directory (or, you can install `pip` and use the above command)

## Step 4: Running the Game
You can run the game by calling `python3 game.py` when you're in the game installation directory (or add a shortcut of some sort).
