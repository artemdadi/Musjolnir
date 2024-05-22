#pylib
from math import *
from time import *
from ctypes import *
import os
import sys

#SDL
from sdl2 import *
from sdl2.sdlimage import *
from sdl2.sdlttf import *
from sdl2.pixels import SDL_Color
from sdl2.stdinc import SDL_calloc, SDL_free

#mylib
from App import *
from SDL_Consts import *
from Sound import *
from String import *

class SDL_app:
    
    def __init__(self, name):
        self.last_time = time()
        self.name = name
        self.app = App(self)
        self.timers = []
        self.last_sound_id = 0
        self.func_times = {}
        self.vert_count = 100
        
    def load_image(self, file_name):
        io = SDL_RWFromFile(file_name, "rb")
        SDL_RWclose(io)
        
    #DEBUG SYSTEM--------------------
    
    def function_time(self, func, name, *args, **kwargs):
    	start = time()
    	result = func(*args, **kwargs)
    	end = time()
    	self.func_times[name] = end - start
    	return result
    
    #AUDIO SYSTEM---------------------------------------------------------------------------------
    
    def init_playing_sounds_buf(self, max_sounds):
        size_of_buf = sizeof(PlayingSound) * max_sounds + sizeof(PlayingSoundInfo)
        self.audio_p = SDL_calloc(c_size_t(size_of_buf), c_size_t(1))
        memset(self.audio_p, 0, size_of_buf)
        self.play_info_p = cast(c_void_p(self.audio_p), POINTER(PlayingSoundInfo))
        self.audio = p_add_cast(self.play_info_p, sizeof(PlayingSoundInfo), PlayingSound)
        self.play_info = self.play_info_p.contents
        self.play_info.max_sounds = max_sounds
        self.play_info.is_playing = False
    
    def make_want_as(self):
        self.want_as = SDL_AudioSpec(0,0,0,0)
        self.want_as.freq = 44100
        self.want_as.format = AUDIO_F32
        self.want_as.channels = 2
        self.want_as.samples = Uint16(4096)
        self.want_as.callback = SDL_AudioCallback_my
        self.want_as.userdata = self.audio_p
        
    def add_sound(self, sound, loop = False, sync_id = None):
        SDL_LockAudio()
        for i in range(self.play_info.max_sounds):
            if self.audio[i].active == False:
                self.audio[i].active = True
                self.audio[i].buf_p = sound.buf_p
                self.audio[i].size = sound.bytes_to_frames(sound.size)*2
                self.audio[i].loop = loop
                if sync_id != None:
                    for i_1 in range(self.play_info.max_sounds):
                        if self.audio[i_1].id == sync_id:
                            self.audio[i].position =  self.audio[i_1].position % sound.size.value
                        break
                self.audio[i].id = self.last_sound_id
                self.last_sound_id+=1
                break
        SDL_UnlockAudio()
        self.last_sound = sound
        return self.audio[i].id
        
    def remove_sound(self, id):
        SDL_LockAudio()
        for i in range(self.play_info.max_sounds):
            if self.audio[i].id == id:
                if self.audio[i].loop == True:
                    self.audio[i].loop = False
                else:
                    self.audio[i].clear()
                break
        SDL_UnlockAudio()
                
    def remove_all_sounds(self):
        SDL_LockAudio()
        for i in range(self.play_info.max_sounds):
            self.audio[i].clear()
        SDL_UnlockAudio()

    #VIDEO SYSTEM--------------------------------------------------------------------------------------------------
    
    def normalize(self, x, y):
        return x/self.width, y/self.height

    def norm_x(self, x):
        return x/self.width
    
    def norm_y(self, y):
        return y/self.height
        
    def norm_to_pixels(self, x, y):
        x = int(x*self.width)
        y = int(y*self.height)
        return x, y

    def norm_to_min_length_pixels(self, value):
        return int(self.min_length * value)

    def draw_widget(self, widget):
        if widget.is_complex():
            for cwidget in widget.widgets:
                self.function_time(self.draw_widget, cwidget.__class__, cwidget)
        else:
            x, y = self.norm_to_pixels(widget.x, widget.y)
            w, h = self.norm_to_pixels(widget.w, widget.h)
            color = widget.color
            if isinstance(widget, Fill_Rect):
                if widget.r == None:
                    self.fill_rect(x, y, w, h, color)
                else:
                    self.fill_rounded_rect(x, y, w, h, widget.r, color)
            elif isinstance(widget, Draw_Rect):
                line_width = self.norm_to_min_length_pixels(widget.line_width)
                if widget.r == None:
                    self.draw_rect(x, y, w, h, line_width, color)
                else:
                    self.draw_rounded_rect(x, y, w, h, line_width, widget.r, color)
            elif isinstance(widget, Text):
                if widget.text != "":
                    self.render_text_in_rect(x, y, w, h, widget.text, color, self.big_font, widget.angle, widget)
            elif isinstance(widget, Diagram):
                self.render_diagram(x, y, w, h, widget.points, color, widget)
            
    #SURFACE CACHE------------------------------------------------------------------
        
    def cached_surf(draw_func):
        def wrapper(*args, **kwargs):
            widget = args[-1]
            self = args[0]
            if hasattr(widget, 'SDL_cache'):
                if widget.is_transformed:
                    self.free_SDL_cache(widget)
                    surfs = draw_func(*args, **kwargs)
                    widget.SDL_cache = surfs
                    widget.is_transformed = False
                else:
                    for s in widget.SDL_cache:
                        surf = s[0]
                        x = s[1]
                        y = s[2]
                        angle = s[3]
                        self.render_surface(surf, x, y, angle)
            else:
                surfs = draw_func(*args, **kwargs)
                widget.SDL_cache = surfs
                widget.clear_func = lambda widget: widget.app.api.free_SDL_cache(widget)
        return wrapper
        
    def free_SDL_cache(self, widget):
        for s in widget.SDL_cache:
            SDL_FreeSurface(s[0])
        delattr(widget, 'SDL_cache')
            
    #DRAWING FUNCS FOR DIFFERENT WIDGETS------------------------------------------------------------------
            
    def fill_rect(self, x, y, w, h, color):
        r, g, b, a = color.unwrap()
        SDL_SetRenderDrawColor(self.renderer, r, g, b, a)
        SDL_RenderFillRect(self.renderer, byref(SDL_Rect(x, y, w, h)))
        
    def draw_rect(self, x, y, w, h, line_width, color):
        r, g, b, a = color.unwrap()
        py_rects = [
            SDL_Rect(x, y, w, line_width),
            SDL_Rect(x, y, line_width, h),
            SDL_Rect(x+w-line_width, y, line_width, h),
            SDL_Rect(x, y+h-line_width, w, line_width)
            ]
        rects = (SDL_Rect * len(py_rects))(*py_rects)
        SDL_SetRenderDrawColor(self.renderer, r, g, b, a)
        SDL_RenderFillRects(self.renderer, rects, len(py_rects))

    def draw_rounded_rect(self, x, y, w, h, line_width, rad, color):
        r, g, b, a = color.unwrap()
        py_rects = [
            SDL_Rect(x + rad, y, w - rad * 2, line_width),
            SDL_Rect(x, y + rad, line_width, h - rad * 2),
            SDL_Rect(x + w - line_width, y + rad, line_width, h - 2 * rad),
            SDL_Rect(x + rad, y + h - line_width, w - 2 * rad, line_width)
            ]
        rects = (SDL_Rect * len(py_rects))(*py_rects)
        SDL_SetRenderDrawColor(self.renderer, r, g, b, a)
        SDL_RenderFillRects(self.renderer, rects, len(py_rects))
        r0 = rad - line_width
        self.draw_circle(x + rad, y + rad, rad, color, start = 180, end = 275, r0 = r0)
        self.draw_circle(x + w - rad, y + rad, rad, color, start = 90, end = 185 , r0 = r0)
        self.draw_circle(x + rad, y + h - rad, rad, color, start = 270, end = 365, r0 = r0)
        self.draw_circle(x + w - rad, y + h - rad, rad, color, start = 0, end = 95, r0 = r0)

    def fill_rounded_rect(self, x, y, w, h, rad, color):
        self.fill_rect(x + rad, y, w - 2 * rad, h, color)
        self.fill_rect(x, y + rad, w, h - 2 * rad, color)
        self.draw_circle(x + rad, y + rad, rad, color, start = 180, end = 270)
        self.draw_circle(x + w - rad, y + rad, rad, color, start = 90, end = 180)
        self.draw_circle(x + rad, y + h - rad, rad, color, start = 270, end = 360)
        self.draw_circle(x + w - rad, y + h - rad, rad, color, start = 0, end = 90)
        

    def draw_circle(self, x0, y0, r, color, start = 0, end = 360, r0 = 0):
        py_vertices = []
        start = radians(start)
        end = radians(end)
        ratio = (end-start) / (2 * pi)
        vert_count = int(self.vert_count * ratio)
        step = 1/self.vert_count
        if (r0 == 0):
            x = x0 + sin(start) * r
            y = y0 + cos(start) * r
            for i in range(vert_count):
                x_next = x0 + sin(start + 2 * pi * (i+1) * step) * r
                y_next = y0 + cos(start + 2 * pi * (i+1) * step) * r
                    
                py_vertices.append(SDL_Vertex(SDL_FPoint(x0, y0), color.unwrap(), SDL_FPoint(0, 0)))
                py_vertices.append(SDL_Vertex(SDL_FPoint(x, y), color.unwrap(), SDL_FPoint(0, 0)))
                py_vertices.append(SDL_Vertex(SDL_FPoint(x_next, y_next), color.unwrap(), SDL_FPoint(0, 0)))

                x, y = x_next, y_next
        else:
            x1 = x0 + sin(start) * r
            y1 = y0 + cos(start) * r
            x2 = x0 + sin(start) * r0
            y2 = y0 + cos(start) * r0
            for i in range(vert_count):
                if i%2 == 0:
                    x_next = x0 + sin(start + 2 * pi * (i+1) * step) * r
                    y_next = y0 + cos(start + 2 * pi * (i+1) * step) * r
                else:
                    x_next = x0 + sin(start + 2 * pi * i * step) * r0
                    y_next = y0 + cos(start + 2 * pi * i * step) * r0
                    
                py_vertices.append(SDL_Vertex(SDL_FPoint(x1, y1), color.unwrap(), SDL_FPoint(0, 0)))
                py_vertices.append(SDL_Vertex(SDL_FPoint(x2, y2), color.unwrap(), SDL_FPoint(0, 0)))
                py_vertices.append(SDL_Vertex(SDL_FPoint(x_next, y_next), color.unwrap(), SDL_FPoint(0, 0)))

                x1, y1 = x2, y2
                x2, y2 = x_next, y_next
            
        vertices = (SDL_Vertex * len(py_vertices))(*py_vertices)
        SDL_RenderGeometry(self.renderer, None, vertices, len(py_vertices), None, 0)
        
    @cached_surf
    def render_diagram(self, x, y, w, h, points, color, widget):
        surf = self.make_diagram_surf(w, h, points, color)
        self.render_surface(surf, x, y)
        return [[surf, x, y, None]]

    #points <= w
    def make_diagram_surf(self, w, h, points, color):
        max_point = 1
        bg_color = Color("invis").as_uint32()
        draw_color = color.as_uint32()
        center = int(h/2)
        surf = SDL_CreateRGBSurfaceWithFormat(0, w, h, 32, SDL_Pixel_Types["SDL_PF_argb8888"])
        SDL_LockSurface(surf)
        p = cast(surf.contents.pixels, POINTER(Uint32))
        for surf_x in range(len(points)):
            point = points[surf_x]
            for surf_y in range(int(((abs(point)/max_point) * center))):
                i = (center + int(copysign(1, point))*surf_y) * w + surf_x
                p[i] = draw_color
        SDL_UnlockSurface(surf)
        blend_mode = SDL_BlendMode(0x00000001)
        SDL_SetSurfaceBlendMode(surf, blend_mode)
        return surf
        
    @cached_surf
    def render_text_in_rect(self, x, y, w, h, text, color, font, angle, widget):
        if angle == 90:
            x+=w
            w, h = h, w
        surfs = []
        buf = StrBuf(text)
        bufs, coords = self.split_text_in_rect(w, h, buf, font)
        if angle == 90:
            r_y = coords[-1][0]
            for i in range(len(bufs)):
                r_x = coords[i][0]
                surf = self.render_text(bufs[i].ushort_p, x - r_y, y + r_x, color, font, angle)
                surfs.append([surf, x - r_y, y + r_x, angle])
                r_y += coords[i][1] + coords[-1][1]
        else:
            r_y = coords[-1][0]
            for i in range(len(bufs)):
                r_x = coords[i][0]
                surf = self.render_text(bufs[i].ushort_p, x + r_x, y + r_y, color, font, angle)
                surfs.append([surf, x + r_x, y + r_y, angle])
                r_y += coords[i][1] + coords[-1][1]
        return surfs

    def split_text_in_rect(self, w, h, buf, font):
        text_w, text_h = buf.get_text_wh(font)
        line_gap = int(text_h/20)
        text_w = 0
        bufs = []
        coords = []
        sum_text_h = 0
        last_stop = 0
        for i in range(buf.text_len):
            char = c_uint16(bytes(buf.text[i], 'UTF-8')[0])
            if TTF_GlyphIsProvided(self.big_font, char):
                maxx = c_int(0)
                minx = c_int(0)
                miny = c_int(0)
                maxy = c_int(0)
                advance = c_int(0)
                TTF_GlyphMetrics(font, char, byref(minx), byref(maxx), byref(miny), byref(maxy), byref(advance))
                if text_w+advance.value > w:
                    x = int(w/2) - int(text_w/2)
                    bufs.append(buf[last_stop:i+1])
                    coords.append([x, text_h])
                    sum_text_h += text_h + line_gap
                    text_w = advance.value
                    last_stop = i + 1
                elif i == (buf.text_len - 1):
                    text_w += advance.value
                    x = int(w/2) - int(text_w/2)
                    bufs.append(buf[last_stop:i+1])
                    coords.append([x, text_h])
                    sum_text_h += text_h + line_gap
                else:
                    text_w += advance.value
            else:
                print("No glyph for '" + buf.text[i] + "'")   
        y = int(h/2) - int((sum_text_h/2 + line_gap * 0.5 *(len(bufs) - 1)))
        coords.append([y, line_gap])
        return bufs, coords
        
    def render_text(self, text, x, y, color, font, angle):
        r, g, b, a = color.unwrap()
        color = SDL_Color(r, g, b, 255)
        surf = TTF_RenderUNICODE_Blended(font, text, color)
        self.render_surface(surf, x, y, angle)
        return surf
        
    def render_surface(self, surface, x, y, angle  = None):
        texture = SDL_CreateTextureFromSurface(self.renderer, surface)
        w = c_int()
        h = c_int()
        SDL_QueryTexture(texture, None, None, byref(w), byref(h))
        self.render_texture(texture, x, y, w, h, angle)
        SDL_DestroyTexture(texture)
            
    def render_texture(self, texture, x, y, w, h, angle = None):
        srcrect = SDL_Rect(0, 0, w, h)
        if angle == None:
            dstrect = SDL_Rect(x, y, w, h)
            SDL_RenderCopy(self.renderer, texture, byref(srcrect), byref(dstrect))
        else:
            dstrect = SDL_Rect(x, y, w, h)
            center = SDL_Point(0, 0)#c_int(int(w.value/2)), c_int(int(h.value/2)))
            SDL_RenderCopyEx(self.renderer, texture, byref(srcrect), byref(dstrect), angle, byref(center), 0)

    #EVENT SYSTEM--------------------------------------------------------------------------------------------
        
    def handle_events(self):
        events = []
        event = SDL_Event()
        while SDL_PollEvent(byref(event)):
            event_type = get_name_by_value(SDL_Events, event.type)
            if event_type == "SDL_WINDOWEVENT":
                pass#print(event.window.event)
            elif event_type == "SDL_QUIT":
                events.append(App_event('END'))
            elif event_type == "SDL_FINGERDOWN":
                events.append(App_event('CLICK', event.tfinger.x, event.tfinger.y))
            elif event_type == "SDL_FINGERUP":
                events.append(App_event('UNCLICK', event.tfinger.x, event.tfinger.y))
            elif event_type == "SDL_MOUSEBUTTONDOWN":
                events.append(App_event('CLICK', self.norm_x(event.button.x), self.norm_y(event.button.y)))
            elif event_type == "SDL_MOUSEBUTTONUP":
                events.append(App_event('UNCLICK', self.norm_x(event.button.x), self.norm_y(event.button.y)))
            elif event_type == 'SDL_RENDER_TARGETS_RESET':
                w = c_int()
                h = c_int()
                SDL_GetWindowSize(self.window, byref(w), byref(h))
                self.width = w.value
                self.height = h.value
                self.app.destroy()
            else:
                pass#print(event_type)
        return events

    def send_event(self, app_event):
        sdl_event = SDL_Event()
        sdl_event.type = SDL_Events[get_name_by_value(SDL_to_app_events, app_event.type)]
        SDL_PushEvent(byref(sdl_event))
    
    def make_timer(self, lat, func):
        act_time = time() + lat
        self.timers.append([act_time, func])
        
    def handle_timers(self, cur_time):
        for timer in self.timers:
            if timer[0] < cur_time:
                timer[1](self)
        for timer in list(self.timers):
            if timer[0] < cur_time:
                self.timers.remove(timer)
        
    #RUN TIME SYSTEM----------------------------------------------------------------------------------------
    
    def run(self):
        #SDL init
        SDL_Init(SDL_INIT_EVERYTHING)
        #IMG_Init()
        TTF_Init()
        self.big_font = TTF_OpenFont(b'Fonts/font.ttf', 40)
        self.small_font = TTF_OpenFont(b'Fonts/font.ttf', 20)
        #window
        c_name = c_char_p(self.name)
        self.window = SDL_CreateWindow(c_name, 30, 30, 800, 500, SDL_WINDOW_SHOWN | SDL_WINDOW_RESIZABLE)
        w = c_int()
        h = c_int()
        SDL_GetWindowSize(self.window, byref(w), byref(h))
        self.width = w.value
        self.height = h.value
        self.display_horizontal = True if self.width > self.height else False
        self.min_length = self.height if self.width > self.height else self.width
        #renderer
        self.renderer = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_ACCELERATED)
        #audio
        self.init_playing_sounds_buf(10)
        self.make_want_as()
        self.have_as = SDL_AudioSpec(0,0,0,0)
        SDL_OpenAudio(byref(self.want_as), byref(self.have_as))
        self.sounds = make_sound_dict(list(Notes_files), "wav", self.want_as)
        # init error
        print("SDL init error: {}".format(SDL_GetError()))
        #additional vars
        self.frame_time = 1
        self.my_widgets = [Text(self.app, None, 0.1, 0.1, 0.9, 0.9, "111222333444555666777888999", Color("red"))]
        self.debug_info = ""
        #app main loop
        SDL_PauseAudio(0)
        run = True
        self.frame = 1
        self.tick_time = 0
        self.tick_per_second = 5
        self.second_per_tick = 1/self.tick_per_second
        self.tick = 0
        while run:
            #begin time
            begin_time = time()
            self.handle_timers(begin_time)
            fps = 1/self.frame_time
            #handle events and update app
            run, main_widget = self.app.update(self.handle_events())
            #video
            SDL_RenderClear(self.renderer)
            self.draw_widget(main_widget)
##            if self.frame == 1:
##            	self.my_widgets[0].change_text(str(self.func_times))#str(fps))
##            for i in self.my_widgets:
##                self.draw_widget(i)
            SDL_RenderPresent(self.renderer)
            #audio
            
            #end time
            self.frame_time = time() - begin_time
            self.last_time = time()
            if self.frame_time == 0:
                self.frame_time = sys.float_info.min
            self.frame+=1
            self.tick_time += self.frame_time
            if self.tick_time > self.second_per_tick:
                self.tick_time = 0
                self.tick+=1
        self.close()
        
    def close(self):
        SDL_PauseAudio(1)
        self.app.destroy()
        self.sounds = 0
        SDL_free(self.audio_p)
        TTF_CloseFont(self.big_font)
        TTF_CloseFont(self.small_font)
        TTF_Quit()
        SDL_CloseAudio()
        SDL_AudioQuit()
        SDL_DestroyRenderer(self.renderer)
        SDL_DestroyWindow(self.window)
        print("Last SDL error:{}".format(SDL_GetError()))
        SDL_Quit()
        
if __name__ == "__main__":
    myapp = SDL_app(b'Music')
    myapp.run()
    
