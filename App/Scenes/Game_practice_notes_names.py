from ..Widget import *
from ..Music_theory import *

import random

class Game_practice_notes_names(Scene):

    def __init__(self, app):
        Scene.__init__(self, app)
        self.gamma = Melody(Note("До", 0), "harmonic", 12)
        notes = self.make_notes()

        def b_back_cb(self):
            self.app.scene_type = "Menu"

        def b_guess_cb(self):
            scene = self.app.scene
            grid = scene.widgets[-1]
            for i in range(4):
                widget = grid.widgets[i]
                if widget.get_text() == scene.next_note:
                    widget.change_color(Color("green"))
                elif widget == self:
                    widget.change_color(Color("red"))

        def b_next_round_cb(self):
            scene = self.app.scene
            notes = scene.make_notes()
            grid = scene.widgets[-1]
            scene.widgets[1].change_text(f"Угадайте следующую ноту: {self.parrent.note}")
            for i in range(len(notes)):
                grid.widgets[i].change_text(notes[i])
                grid.widgets[i].change_color(Color("random"))
                
        self.widgets.append(Label(app, self, 0.1, 0.1, 0.8, 0.2, f"Угадайте следующую ноту: {self.note}", Color("white"), Color(BUTTON_COLOR)))
        self.widgets.append(Button(app, self, 0.1, 0.55, 0.8, 0.15, Color("random"), "Следующий раунд", unclick_func=b_next_round_cb))
        self.widgets.append(Button(app, self, 0.1, 0.75, 0.8, 0.15, Color("random"), "Назад", unclick_func=b_back_cb))
        
        unclick_funcs = [b_guess_cb for i in range(4)]
        colors = [Color(BUTTON_COLOR) for i in range(4)]
        self.widgets.append(Button_grid(app, self, 0.1, 0.35, 0.8, 0.15, 0.05, 0, 4, 1, notes, colors, unclick_funcs))

    def make_notes(self):
        result = []
        self.note = random.choice(self.gamma.notes)
        self.next_note = self.note.new_from_interval("Полутон")
        self.other_notes = self.gamma.str_list()
        self.note = str(self.note)
        self.next_note = str(self.next_note)
        self.other_notes.remove(self.note)
        self.other_notes.remove(self.next_note)
        self.other_notes = random.sample(self.other_notes, 3)
        result = self.other_notes + [self.next_note]
        random.shuffle(result)
        return result
