from ..Widget import *

class Notes_check(Scene):
    
    def __init__(self, app):
        Scene.__init__(self, app)
        
        def b_back_cb(self):
            self.app.scene_type = "Settings"

        def make_diagram(self):
            sound = self.parrent.sounds[self.get_text()]
            self.parrent.widgets.append(Diagram_widget(app, self.parrent, 0.1, 0.1, 0.8, 0.8, sound.get_as_points(), Color("purple")))

        self.sounds = app.api.sounds
        sounds_names = list(self.sounds.keys())
        columns = 6
        raws = 4
        unclick_funcs = [make_diagram for i in range(columns*raws)]
        self.make_buttons_grid(0.1, 0.1, 0.8, 0.6, columns, raws, sounds_names, unclick_funcs)
        
        self.widgets.append(Button(app, self, 0.2, 0.8, 0.6, 0.1, Color("random"), "Назад", unclick_func=b_back_cb))
