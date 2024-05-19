from .Scenes import *
from .Color import *

class App_event:

    event_types = ['END', 'CLICK', 'UNCLICK']

    def __init__(self, event_type, x = None, y = None):
        self.type = event_type
        self.x = x
        self.y = y

class App:

    game_types = Game_types

    def __init__(self, api):
        self.api = api
        self.color_theme = "default"
        self.scene_type = "Menu"
        self.last_scene_type = self.scene_type
        self.game_type = self.game_types[1]
        self.scene = Scenes[self.scene_type](self)

    def handle_events(self, events):
        run = True
        for event in events:
            if event.type == 'END':
                run = False
            if event.type == 'CLICK':
                self.last_active_widget = self.scene.find_first_interactive_widget(event.x, event.y)
                if self.last_active_widget != None:
                    self.last_active_widget.activate()  
            elif event.type == 'UNCLICK':
                if self.last_active_widget!= None:
                    self.last_active_widget.disactivate(self.scene.is_widget(event.x, event.y, self.last_active_widget))
        return run

    def update(self, events):
        run = self.handle_events(events)
        if self.scene.have_cb():
            self.scene()
        if self.scene_type != self.last_scene_type:
            self.last_scene_type = self.scene_type
            #self.remove_all_sounds()
            self.scene.destroy()
            self.scene = Scenes[self.scene_type](self)
        return run, self.scene

    def send_event_to_api(self, event):
        self.api.send_event(event)

    def stop(self):
        self.send_event_to_api(App_event("END"))

    def destroy(self):
        self.scene.destroy()
