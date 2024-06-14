from .Menu import *
from .Game import *
from .Piano import *
from .Settings import *
from .Notes_check import *

Scenes_names = ["Menu", "Piano", "Settings", "Notes_check", "Game"]
Scenes = {}
for i in Scenes_names:
    Scenes[i] = locals()[i]
