from ..Widget import *

class Menu(Scene):
    
    def __init__(self, app):
        Scene.__init__(self, app)
        
        def b_change_scene_cb(self):
            if self.value == "Game":
                self.app.scene_type = self.app.game_type
            else:
                self.app.scene_type = self.value
        
        def b_exit_cb(self):
            self.app.stop()
        
        scenes = ["Game", "Piano", "Settings"]
        b_names = ["Новая игра", "Клавиши", "Настройки", "Выход"]
        button_count = len(b_names)
        unclick_funcs = [b_change_scene_cb for i in range(len(scenes))] + [b_exit_cb]
        scenes+= [None]
        self.widgets.append(Button_grid(app, self, 0.1, 0.1, 0.8, 0.8, 0, 0.05, 1,
                                        button_count, b_names, unclick_funcs = unclick_funcs,
                                        values = scenes, rad = 20))
