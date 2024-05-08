from random import randrange
from sdl2.pixels import SDL_Color
from sdl2 import SDL_SetPaletteColors
from .Math import add_in_range
    
def fill_colors_palette(palette_p, colors):
    n = len(colors)
    c_colors = (SDL_Color * n)()
    for i in range(n):
        c_colors[i].r = colors[i].r
        c_colors[i].g = colors[i].g
        c_colors[i].b = colors[i].b
        c_colors[i].a = colors[i].a
    return SDL_SetPaletteColors(palette_p, c_colors, 0, n)

COLOR_THEMES = {
"default": {
    "Background" : "#16171b",
    "Button" : "#01b075"
    }
}

class Color:
    
    colors = {
    "red": (255, 0, 0, 255),
    "green": (0, 255, 0, 255),
    "blue": (0,0,255, 255),
    "black": (0,0,0, 255),
    "gray": (128,128,128, 255),
    "white":(255,255,255, 255),
    "purple":(255,0,255, 255),
    "invis":(255,0,0, 0)
    }
    
    def __init__(self, in_var = None, r = 0, g = 0, b = 0, a = 255, theme = None):
        if theme != None:
            in_var = COLOR_THEMES[theme][in_var]
        if isinstance(in_var, str):
            if in_var == "random":
                r, g, b = self.random_color()
            elif in_var[0] == "#":
                r, g, b = int(in_var[1:3], 16), int(in_var[3:5], 16), int(in_var[5:7], 16)
            else:
                r, g, b, a = self.colors[in_var]
        elif isinstance(in_var, tuple):
            r, g, b, a = in_var
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        
    def __str__(self):
        return "Color(r={}, g={}, b={}, a={})".format(self.r,self.b,self.g, self.a)
        
    def random_color(self):
        return randrange(0,255), randrange(0,255), randrange(0,255)
        
    def unwrap(self):
        return self.r, self.g, self.b, self.a
        
    def add_k(self, k):
        r = add_in_range(self.r, k, 0, 255)
        g = add_in_range(self.g, k, 0, 255)
        b = add_in_range(self.b, k, 0, 255)
        return Color(r, g, b, self.a)
        
    def invert(self):
        r = 255 - self.r
        g = 255 - self.g
        b = 255 - self.b
        return Color(r, g, b, self.a)
        
    def as_uint32(self):
        return ((self.a << 24)|(self.r << 16)|(self.g << 8)|(self.b <<0))
