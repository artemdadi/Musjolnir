from ..Widget import *

class Settings(Scene):
    
    def __init__(self, app):
        Scene.__init__(self, app)

        def b_change_scene(self):
            self.app.scene_type = self.next_scene

        def b_test(self):
            self.app.api.add_sound(self.app.api.sounds['Фа3'])

        self.widgets.append(Text(app, self, 0.1, 0.2, 0.8, 0.1, "Выбирите тип игры", Color("black")))
        self.widgets.append(Choose_menu(app, self, 0.1, 0.3, 0.8, 0.1, Color("random"), "game_type", app.game_types))
        self.widgets.append(Button(app, self, 0.2, 0.6, 0.6, 0.1, Color("random"), "Проверка нот", unclick_func=b_change_scene))
        self.widgets[-1].next_scene = "Notes_check"
        self.widgets.append(Button(app, self, 0.2, 0.7, 0.6, 0.1, Color("random"), "Тест", unclick_func=b_test))
                       
        self.widgets.append(Button(app, self, 0.2, 0.8, 0.6, 0.1, Color("random"), "Назад", unclick_func=b_change_scene))
        self.widgets[-1].next_scene = "Menu"
                       
