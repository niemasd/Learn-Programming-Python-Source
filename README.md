This repository contains the source code of the game engine behind [Learn Programming: Python](https://store.steampowered.com/app/1536770/Learn_Programming_Python/). The two key files are [`game.py`](game.py) (the main source of the game) and [`universal.py`](universal.py) (a helper file).

If you have already purchased the game, you can simply drop these files into the game installation directory, and they should be able to load the lesson data just fine. To locate the game's installation directory, you can do the following:

1. Open Steam
2. Click on the "Learn Programming: Python" game in your Steam library
3. Click on the gear button at the top-right of the page (directly under the game banner)
4. Highlight the "Manage" menu, and click "Browse local files"
5. The folder that Steam opens is the game's installation directory
    * You can drop `game.py` and `universal.py` in this folder, and then you can simply double-click `game.py` to play!

This open source game engine should work on any platform (not just Windows). To run it on non-Windows operating systems, you may need to comment out [line 220 of `game.py`](game.py#L220), which I believe uses Windows-specific commands to make the window full-screen.

Enjoy :-)
