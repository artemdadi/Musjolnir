from ..Widget import *
from ..Music_theory import *

class Game_guess_note_with_sound(Scene):	

    def __init__(self, app):
        Scene.__init__(self, app)
        b_h = 0.8/5
        self.sound_id = 0
        def play_note(self):
            self.sound_id = self.scene.app.add_sound(self.scene.app.sounds[self.note.name], True)
                
        def end_play(self):
            self.scene.app.remove_sound(self.sound_id)
                
        def b_back_cb(self):
            self.app.scene_type = "Menu"
                
        self.widgets.append(Button(app, self, 0.1, 0.1, 0.8, b_h, Color("random"), "Сыграть гамму", click_func=play_note, unclick_func=end_play))
        self.widgets.append(Button(app, self, 0.1, 0.1 + b_h, 0.8, b_h, Color("random"), "Сыграть ноту", click_func=play_note, unclick_func=end_play))

        gamma = Melody(Note("До", 3), "major")

        x = 0.05
        b_w = (1 - x * 2)/(len(gamma.notes)-1)
        for n in gamma.notes[:-1]:
            self.widgets.append(Button(app, self, x, 0.5, b_w, 0.1, Color("random"), n.name[:-1], click_func=play_note, unclick_func=end_play))
            x+=b_w
            self.widgets[-1].note = n
                
        self.widgets.append(Button(app, self, 0.1, 0.7, 0.8, 0.1, Color("random"), "Следующий уровень", unclick_func=b_back_cb))           
        self.widgets.append(Button(app, self, 0.1, 0.8, 0.8, 0.1, Color("random"), "Назад", unclick_func=b_back_cb))
