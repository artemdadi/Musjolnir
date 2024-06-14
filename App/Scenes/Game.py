from ..Widget import *

class Game(Scene):
    
    def __init__(self, app):
        Scene.__init__(self, app)
        #remove bg
        self.pop_last_widget()
        
        Game = app.games[app.game_type](app)
        self.widgets.append(Game)
