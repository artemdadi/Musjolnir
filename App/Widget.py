from .Color import *
from .Math import dir_to_angle
from .Config import *
from .Geometry import *

class Widget:

    dimension_attrs = ["x", "y", "w", "h"]
    transform_attrs = dimension_attrs + ["color", "angle"]
    widget_names = ["bg"]
    
    def __init__(self, app, parrent, geometry, color = None, is_interactive = False, coordinate_mod = 0):
        if isinstance(geometry, tuple):
            self.geometry = Rect(Point(geometry[0], geometry[1]), Size(geometry[2], geometry[3]))
        else:
            self.geometry = geometry
        self.coordinate_mod = coordinate_mod
        if coordinate_mod == 1:
            self.geometry = self.geometry.scale(parrent.geometry)
        self.visible = True
        self.app = app
        self.parrent = parrent
        self.is_transformed = False
        self.color = color #if color != None else Color(type(self).__name__, theme = app.color_theme)
        self.widgets = []
        self.is_interactive = is_interactive

    def __setattr__(self, name, value):
        if name in self.transform_attrs: 
            self.is_transformed = True
        if (value == False) and (name == "visible") and (self.visible == True):
            self.destroy()
        object.__setattr__(self, name, value)

    def __getitem__(self, key):
        return self.widgets[self.widget_names.index(key)]

    def __setitem__(self, key, value):
        self.widgets[self.widget_names.index(key)] = value

    def __str__(self):
        return self.__class__.__name__ + str(self.__dict__)

    def is_complex(self):
        if len(self.widgets) == 0:
            return False
        else:
            return True
    
    def is_widget(self, x, y):
        if isinstance(self.geometry, Rect):
            return self.geometry.is_point_in_rect(Point(x, y))
        
    def find_first_interactive_widget(self, x, y):
        for w in self.widgets[::-1]:
            if w.is_widget(x, y):
                if w.is_interactive:
                    return w
                else:
                    if w.is_complex:
                        return w.find_first_interactive_widget(x, y)
        return None

    def add_border(self, w, h):
        self.is_transformed = True
        if isinstance(self.geometry, Rect):
            self.geometry.add_border(Size(w,h))

    def destroy(self):
        if self.is_complex():
            for w in self.widgets:
                w.destroy()
        if hasattr(self, "clear_func"):
            self.clear_func(self)

    def pop_last_widget(self):
        self.widgets[-1].destroy()
        self.widgets.pop()

    def pop_widget(self, widget):
        widget.destroy()
        self.widgets.pop(self.widgets.index(widget))

    #ELEMENTARY WIDGETS---------------------------------------------------------

class Fill_Rect(Widget):
    
    def __init__(self, app, parrent, geometry, color, r = None, coordinate_mod = 0):
        Widget.__init__(self, app, parrent, geometry, color, coordinate_mod = coordinate_mod)
        self.r = r
        
class Draw_Rect(Widget):
    
    def __init__(self, app, parrent, geometry, line_width, color, r = None, coordinate_mod = 0):
        Widget.__init__(self, app, parrent, geometry, color, coordinate_mod = coordinate_mod)
        self.line_width = line_width
        self.r = r

class Fill_Triangle(Widget):
    
    def __init__(self, app, parrent, x, y, x1, y1, x2, y2, color):
        Widget.__init__(self, app, parrent, x, y, color = color)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class Fill_Rect_Triangle(Widget):
    
    def __init__(self, app, parrent, geometry, angle, color, coordinate_mod = 0):
        Widget.__init__(self, app, parrent, geometry, color = color, coordinate_mod = coordinate_mod)
        self.angle = angle
                
class Text(Widget):

    transform_attrs = Widget.transform_attrs + ["text"]
        
    def __init__(self, app, parrent, geometry, text, color = None, direction = None, coordinate_mod = 0):
        Widget.__init__(self, app, parrent, geometry, color, coordinate_mod = coordinate_mod)
        self.text = text
        self.angle = dir_to_angle(direction)
    
    def change_text(self, text):
        self.text = text
        
class Diagram(Widget):

    transform_attrs = Widget.transform_attrs + ["points"]

    def __init__(self, app, parrent, x, y, w, h, points, color = None):
        Widget.__init__(self, app, parrent, x, y, w, h, color)
        self.points = points

    def change_points(self, points):
        self.points = points

    #COMPLEX WIDGETS-------------------------------------------------------

class Scene(Widget):
    
    def __init__(self, app, color = None, widgets = None):
        geometry = Rect(Point(0, 0), Size(1, 1))
        Widget.__init__(self, app, None, geometry)
        color = color if color != None else Color("Scene_bg", theme = app.color_theme)
        self.widgets = [Fill_Rect(app, self, Rect(Point(0, 0), Size(1, 1)), color)]

    def have_cb(self):
        return hasattr(self, "callback")
        
    def __call__(self):
        self.callback(self)

class Label(Widget):

    widget_names = Widget.widget_names + ["text"]

    def __init__(self, app, parrent, geometry, text, text_color = None, bg_color = None):
        Widget.__init__(self, app, parrent, geometry)
        bg_color = bg_color if bg_color != None else Color("Label_bg", theme = app.color_theme)
        text_color = text_color if text_color != None else Color("Label_text", theme = app.color_theme)
        self.widgets = [
            Fill_Rect(app, self, geometry, bg_color),
            Text(app, self, geometry, text, text_color)
        ]
            
    def change_text(self, text):
        self.widgets[1].change_text(text)

class Button(Widget):

    widget_names = Widget.widget_names + ["text", "border", "click_border", "icon"]
    
    def __init__(self, app, parrent, geometry, text, color = None, text_dir = None, border = 0.005,
                 click_border = 0.02, click_func = None, unclick_func = None, r = None, icon = None):
        Widget.__init__(self, app, parrent, geometry, color, is_interactive = True)
        color = color if color != None else Color("Button_bg", theme = app.color_theme)
        self.click_border = click_border
        self.click_func = click_func
        self.unclick_func = unclick_func
        self.widgets = [
            Fill_Rect(app, self, (border, border, 1 - border * 2, 1 - border * 2), color, r, 1),
            Text(app, self, (border, border, 1 - border * 2, 1 - border * 2), text, Color("black"), coordinate_mod = 1),
            Draw_Rect(app, self, (0, 0, 1, 1), border, Color("black"), r, coordinate_mod = 1),
            Draw_Rect(app, self, geometry, click_border, color, r)
        ]
        self["click_border"].visible = False
        self.add_icon(icon)

    def add_icon(self, icon):
        if icon != None:
            self.widgets.append(
                Fill_Rect_Triangle(self.app, self, (0.9, 0.2, 0.1, 0.6), 0, Color("black"), 1)
            )
            temp = self["text"].coordinate_mod
            self["text"].coordinate_mod = 0
            self["text"].geometry["size"]["w"] -= self["icon"].geometry["size"]["w"]
            self["text"].coordinate_mod = temp

    def change_color(self, color = None):
        color = color if color != None else Color("Button_bg", theme = self.app.color_theme)
        self["bg"].color = color

    def get_text(self):
        return self.widgets[1].text

    def change_text(self, text):
        self["text"].change_text(text)
        
    def activate(self):
        if self.click_func != None:
            self.click_func(self)
        self["click_border"].visible = True
        self["bg"].color = self["bg"].color.add_k(-40)
        self["text"].add_border(-self.click_border, -self.click_border)
        self["text"].color = self["text"].color.invert()
        
    def disactivate(self, run_func = True):
        self["text"].add_border(self.click_border, self.click_border)
        self["text"].color = self["text"].color.invert()
        self["bg"].color = self["click_border"].color
        self["click_border"].visible = False
        if (self.unclick_func != None) and run_func:
            self.unclick_func(self)

class Button_grid(Widget):
    
    def __init__(self, app, parrent, geometry, padding_w, padding_h, columns, raws, names,
                 colors = None, unclick_funcs = None, click_funcs = None, values = None, rad = None):
        Widget.__init__(self, app, parrent, geometry)
        if click_funcs   == None: click_funcs = [None for i in range(len(names))]
        if unclick_funcs == None: unclick_funcs = [None for i in range(len(names))]
        if values        == None: values = [None for i in range(len(names))]
        if colors        == None: colors = [None for i in range(len(names))]
        x, y = self.geometry["p"].values
        w, h = self.geometry["size"].values
        b_w = (w - padding_w * (columns - 1))/columns
        b_h = (h - padding_h * (raws - 1))/raws
        ind = 0
        for r in range(raws):
            for c in range(columns):
                self.widgets.append(Button(self.app, self,
                                           (x + c*(b_w + padding_w), y + r*(b_h + padding_h), b_w, b_h),
                                           names[ind], colors[ind],
                                           click_func=click_funcs[ind],
                                           unclick_func=unclick_funcs[ind],
                                           r = rad))
                self.widgets[-1].value = values[ind]
                ind += 1
        
class Diagram_widget(Widget):
        
    def __init__(self, app, parrent, x, y, w, h, points, color = None):
        Widget.__init__(self, app, parrent, x, y, w, h, color)
        self.points = points
        self.size = len(points)
        self.step = 0
        self.pixel_w, self.pixel_h = app.api.norm_to_pixels(w, h)
        self.max_step = int(self.size/self.pixel_w)
##        p = self.size if self.size <= self.pixel_h else self.pixel_h
        def close(self):
            self.parrent.parrent.pop_last_widget()
        def next_step(self):
            self.parrent.change_step(1)
        def prev_step(self):
            pass
            self.parrent.change_step(-1)
        self.widgets = [
            Fill_Rect(app, self, x, y, w, h, Color("black")),
            Diagram(app, self, x, y, w, h, points[:self.pixel_w], color),
            Text(app, self, x, y, 0.2, 0.2, "Step: {}/{}".format(self.step, self.max_step), Color("white")),
            Button(app, self, x      , y + 7*h/8, w/3, h/8, Color("green"), "Назад", unclick_func=close),
            Button(app, self, x + w/3, y + 7*h/8, w/3, h/8, Color("green"), "<<<", unclick_func=prev_step),
            Button(app, self, x + 2*w/3, y + 7*h/8, w/3, h/8, Color("green"), ">>>", unclick_func=next_step)
        ]

    def change_step(self, k):
        self.step = add_in_range(self.step, k, 0, self.max_step)
        p0 = self.pixel_w * self.step
        offset = self.size - p0 if self.step == self.max_step else self.pixel_w
        p1 = p0 + offset
        self.widgets[1].change_points(self.points[p0:p1])
        self.widgets[2].change_text("Step: {}/{}".format(self.step, self.max_step))

class Choose_menu(Widget):

    widget_names = ["button", "options"]

    def __init__(self, app, parrent, geometry, var_name, values, color = None):
        color = color if color != None else Color("Button_bg", theme = app.color_theme)
        Widget.__init__(self, app, parrent, geometry)
        self.var_name = var_name
        
        def b_change_var(b):
            main_widget = b.parrent.parrent
            setattr(b.app, main_widget.var_name, b.value)
            self.widgets[0].change_text(b.value)
            self.h -= self["options"].h
            self["options"].visible = False
            self["button"]["icon"].angle = 0

        unclick_funcs = [b_change_var for i in range(len(values))]
        
        x, y = self.geometry["p"].values
        w, h = self.geometry["size"].values
        padding_h = 0
        grid_h = (h + padding_h) * len(values) - padding_h
        self.widgets = [
            Button(app, self, geometry, getattr(self.app, var_name), color, unclick_func=self.show_options, icon = "triangle"),
            Button_grid(self.app, self,
                        (x, y + h, w, grid_h),
                        0, padding_h, 1, len(values), values,
                        colors = None, unclick_funcs = unclick_funcs, values = values)
        ]
        self["options"].visible = False

    def show_options(self, button):
        self.h += self["options"].h
        self["button"]["icon"].angle = 180
        self["options"].visible = True
        
        
                            
