from .Color import *
from .Math import dir_to_angle
from .Config import *

class Widget:
    
    def __init__(self, app, parrent, x, y, w, h, color = None, is_interactive = False):
        self.app = app
        self.parrent = parrent
        self.is_transformed = False
        self.x = x
        self.h = h
        self.y = y
        self.w = w
        self.color = color #if color != None else Color(type(self).__name__, theme = app.color_theme)
        self.widgets = []
        self.is_interactive = is_interactive

    def is_complex(self):
        if len(self.widgets) == 0:
            return False
        else:
            return True

    def transform(func):
        def wrap(*args, **kwargs):
            self = args[0]
            self.is_transformed = True
            func(*args, **kwargs)
        return wrap
    
    def is_widget(self, x, y, widget):
        if x >= widget.x and x <= (widget.x+widget.w) and y >= widget.y and y <=(widget.y+widget.h):
            return True
        else: 
            return False
        
    def find_first_interactive_widget(self, x, y):
        for w in self.widgets[::-1]:
            if self.is_widget(x, y, w):
                if w.is_interactive:
                    return w
                else:
                    if w.is_complex:
                        return w.find_first_interactive_widget(x, y)
        return None
        
    def bg_color(self, color = None):
        if color == None:
            return self.widgets[0].color
        else:
            self.widgets[0].color = color
            
    @transform
    def add_border(self, w, h):
        self.x -= w
        self.y -= h
        self.w += 2*w
        self.h += 2*h

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

    def print_dimensions(self):
        print('x: {}, y: {}, w: {}, h: {}'.format(self.x, self.y, self.w, self.h))

    #ELEMENTARY WIDGETS---------------------------------------------------------

class Fill_Rect(Widget):
    
    def __init__(self, app, parrent, x, y, w, h, color, r = None):
        Widget.__init__(self, app, parrent, x, y, w, h, color)
        self.r = r
        
class Draw_Rect(Widget):
    
    def __init__(self, app, parrent, x, y, w, h, border, color):
        Widget.__init__(self, app, parrent, x, y, w, h, color)
        self.border = border
                
class Text(Widget):
        
    def __init__(self, app, parrent, x, y, w, h, text, color = None, direction = None):
        Widget.__init__(self, app, parrent, x, y, w, h, color)
        self.text = text
        self.angle = dir_to_angle(direction)
        
    @Widget.transform
    def change_text(self, text):
        self.text = text
        
class Diagram(Widget):

    def __init__(self, app, parrent, x, y, w, h, points, color = None):
        Widget.__init__(self, app, parrent, x, y, w, h, color)
        self.points = points

    @Widget.transform
    def change_points(self, points):
        self.points = points

    #COMPLEX WIDGETS-------------------------------------------------------

class Scene(Widget):
    
    def __init__(self, app, color = None, widgets = None):
        color = color if color != None else Color("Scene_bg", theme = app.color_theme)
        Widget.__init__(self, app, None, 0, 0, 1, 1)
        self.widgets = [Fill_Rect(app, self, 0, 0, 1, 1, color)]

    def have_cb(self):
        return hasattr(self, "callback")
        
    def __call__(self):
        self.callback(self)

class Label(Widget):

    def __init__(self, app, parrent, x, y, w, h, text, text_color, bg_color = None):
        Widget.__init__(self, app, parrent, x, y, w, h, bg_color)
        self.widgets = [Text(app, self, x, y, w, h, text, text_color)]
        if bg_color != None:
            self.widgets = [Fill_Rect(app, self, x, y, w, h, bg_color)] + self.widgets
            
    def change_text(self, text):
        #if bg_color == none [1] is wrong
        self.widgets[1].change_text(text)

class Button(Widget):
    
    def __init__(self, app, parrent, x, y, w, h, text, color = None, text_dir = None, border = None,
                 click_border = 0.01, click_func = None, unclick_func = None, r = None):
        
        Widget.__init__(self, app, parrent, x, y, w, h, color, is_interactive = True)
        color = color if color != None else Color("Button_bg", theme = app.color_theme)
        self.click_border = click_border
        self.click_func = click_func
        self.unclick_func = unclick_func
        self.widgets = [Fill_Rect(app, self, x, y, w, h, color, r),
                        Text(app, self, x, y, w, h, text, Color("black"), text_dir)]
        if border != None:
            self.widgets.append(Draw_Rect(app, self, x, y, w, h, border, Color("black")))

    def change_color(self, color):
        self.widgets[0].color = color

    def get_text(self):
        return self.widgets[1].text

    def change_text(self, text):
        self.widgets[1].change_text(text)
        
    def activate(self):
        if self.click_func != None:
            self.click_func(self)
        self.widgets.append(Draw_Rect(self.app, self, self.x, self.y, self.w, self.h, self.click_border, self.bg_color()))
        self.bg_color(self.widgets[0].color.add_k(-30))
        self.widgets[1].add_border(-self.click_border, -self.click_border)
        self.widgets[1].color = self.widgets[1].color.invert()
        
    def disactivate(self, run_func = True):
        self.widgets[1].add_border(self.click_border, self.click_border)
        self.widgets[1].color = Color("black")
        self.bg_color(self.widgets[-1].color)
        self.pop_last_widget()
        if (self.unclick_func != None) and run_func:
            self.unclick_func(self)

class Button_grid(Widget):
    
    def __init__(self, app, parrent, x, y, w, h, padding_w, padding_h, columns, raws, names,
                 colors = None, unclick_funcs = None, click_funcs = None, values = None, rad = None):
        Widget.__init__(self, app, parrent, x, y, w, h)
        if click_funcs   == None: click_funcs = [None for i in range(len(names))]
        if unclick_funcs == None: unclick_funcs = [None for i in range(len(names))]
        if values        == None: values = [None for i in range(len(names))]
        if colors        == None: colors = [None for i in range(len(names))]
        b_w = (w - padding_w * (columns - 1))/columns
        b_h = (h - padding_h * (raws - 1))/raws
        ind = 0
        for r in range(raws):
            for c in range(columns):
                self.widgets.append(Button(self.app, self,
                                           x + c*(b_w + padding_w), y + r*(b_h + padding_h),
                                           b_w, b_h, names[ind], colors[ind],
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
        self.widgets = [Fill_Rect(app, self, x, y, w, h, Color("black")),
                        Diagram(app, self, x, y, w, h, points[:self.pixel_w], color),
                        Text(app, self, x, y, 0.2, 0.2, "Step: {}/{}".format(self.step, self.max_step), Color("white")),
                        Button(app, self, x      , y + 7*h/8, w/3, h/8, Color("green"), "Назад", unclick_func=close),
                        Button(app, self, x + w/3, y + 7*h/8, w/3, h/8, Color("green"), "<<<", unclick_func=prev_step),
                        Button(app, self, x + 2*w/3, y + 7*h/8, w/3, h/8, Color("green"), ">>>", unclick_func=next_step)]

    def change_step(self, k):
        self.step = add_in_range(self.step, k, 0, self.max_step)
        p0 = self.pixel_w * self.step
        offset = self.size - p0 if self.step == self.max_step else self.pixel_w
        p1 = p0 + offset
        self.widgets[1].change_points(self.points[p0:p1])
        self.widgets[2].change_text("Step: {}/{}".format(self.step, self.max_step))

class Choose_menu(Widget):

    def __init__(self, app, parrent, x, y, w, h, color, var_name, values):
        Widget.__init__(self, app, parrent, x, y, w, h, color)
        self.var_name = var_name
        self.values = values
        self.init_h = self.h
        self.widgets = [Button(app, self, x, y, w, h, getattr(self.app, var_name), color = color, unclick_func=self.show_options)]

    def show_options(self, button):
        def b_change_var(b):
            main_widget = b.parrent.parrent
            setattr(b.app, main_widget.var_name, b.value)
            main_widget.w = b.w
            main_widget.pop_last_widget()
            main_widget.widgets.append(Button(b.app, main_widget, main_widget.x, main_widget.y, b.w, main_widget.init_h, getattr(b.app, main_widget.var_name), unclick_func=main_widget.show_options))

        self.pop_last_widget()
        unclick_funcs = [b_change_var for i in range(len(self.values))]
        self.h = 0.1 * len(self.values)
        self.widgets.append(Button_grid(self.app, self, self.x, self.y, 0.8, self.h, 0.05, 0.05, 1, len(self.values), self.values, colors = None, unclick_funcs = unclick_funcs, values = self.values))
                            
