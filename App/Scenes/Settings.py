from ..Widget import *

class Settings(Scene):

    widget_names = ["label1", "choose1", "button_note", "test", "back"]
    
    def __init__(self, app):
        Scene.__init__(self, app)

        def b_change_scene(self):
            self.app.scene_type = self.next_scene

        def b_test(self):
            self.app.api.add_sound(self.app.api.sounds['Фа3'])

        self.widgets = [
            Label(app, self, (0.1, 0.2, 0.8, 0.1), "Выбирите тип игры"),
            Choose_menu(app, self, (0.1, 0.3, 0.8, 0.1), "game_type", app.game_types),
            Button(app, self, (0.2, 0.6, 0.6, 0.1), "Проверка нот", unclick_func=b_change_scene),
            Button(app, self, (0.2, 0.7, 0.6, 0.1), "Тест", unclick_func=b_test),
            Button(app, self, (0.2, 0.8, 0.6, 0.1), "Назад", unclick_func=b_change_scene)
        ]
        self["button_note"].next_scene = "Notes_check"
        self["back"].next_scene = "Menu"
                       
