from .Menu import *
from .Piano import *
from .Settings import *
from .Notes_check import *
from .Game_guess_note_with_sound import *
from .Game_practice_notes_names import *

Scenes_names = ["Menu", "Piano", "Settings", "Notes_check"]
Game_types = ["Game_guess_note_with_sound", "Game_practice_notes_names"]
Scenes_names += Game_types
Scenes = {}
for i in Scenes_names:
    Scenes[i] = locals()[i]
