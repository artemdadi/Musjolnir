from ..Widget import *
from ..Music_theory import *

class Piano(Scene):
    
    def __init__(self, app):
        Scene.__init__(self, app)
        
        def play_note(self):
            self.sound_id = self.app.api.add_sound(self.app.api.sounds[self.note._str_with_octave()])
            
        def b_back_cb(self):
            self.app.scene_type = "Menu"
        
        gamma = Melody(Note("Фа", 2), "harmonic", 12 * 2)
        black_count = gamma.count_sharps()
        whites_count = len(gamma) - black_count
        #whites
        y = 0.05
        button_height = (1 - y*2) / (whites_count)
        
        for n in gamma.notes:
            if not(n.is_sharp()):
                self.widgets.append(Button(app, self, 0.1, y, 0.4, button_height, Color("white"), "", border = 0.01, click_border = 0.01, click_func=play_note))
                self.widgets[-1].note = n
                y+=button_height
                
        #blacks
        y = 0.05
##        for n in gamma.notes:
##            if n.is_sharp():
##                widgets.append(Button(self, 0.3, y -  button_height/2/2, 0.2, button_height/2, Color("black"), "", border = 0.01, click_border = 0.01, click_func=play_note, unclick_func=end_play))
##                widgets[-1].note = n
##            else:
##                y+=button_height
            
        self.widgets.append(Button(app, self, 0.7, 0.3, 0.2, 0.4, Color("random"), "Назад", unclick_func=b_back_cb))
