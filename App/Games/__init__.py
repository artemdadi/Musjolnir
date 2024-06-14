from .Game_guess_note_with_sound import *
from .Game_practice_notes_names import *

Games_names = ["Game_guess_note_with_sound", "Game_practice_notes_names"]
Games = {}
for i in Games_names:
    Games[i] = locals()[i]
