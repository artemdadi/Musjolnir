from ctypes import *
from sdl2.sdlttf import *
from sdl2.stdinc import SDL_calloc, SDL_free

class StrBuf:
    
    def __init__(self, text):
        self.text  = text
        self.text_len = len(text)
        self.size = len(text) + 1
        self.void_p = SDL_calloc(c_size_t(self.size), c_size_t(2))
        self.ushort_p = cast(self.void_p, POINTER(c_ushort))
        for i in range(len(text)):
            self.insert(text[i], i)
        self.insert("\0", i + 1)
        
    def __str__(self):
        result = ""
        for i in range(self.size):
            if chr(self.ushort_p[i]) == "\0":
                result += str("NULL")
            else:
                result += chr(self.ushort_p[i])
        return result
        
    def __del__(self):
        self.free()
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            if key.start < 0:
                return None
            elif key.stop > (self.size - 1):
                return None
            else:
                result = ""
                for i in range(key.start, key.stop):
                    result+=chr(self.ushort_p[i])
                return StrBuf(result)
        else:
            if key < 0 or key > (self.size - 1):
                return None
            else:
                return StrBuf(chr(self.ushort_p[key]))
                
    def text_slice(start = None, stop = None, step = None):
        return self.text[start, stop, step]
    
    def _insert_pystr_as_ushort(self, pystr, i):
        wchar = c_wchar(pystr)
        c_u_p = cast(pointer(wchar), POINTER(c_ushort))
        self.ushort_p[i] = c_u_p.contents.value
    
    def insert(self, pystr, i):
        self._insert_pystr_as_ushort(pystr, i)
        
    def move_left(self, i):
        for x in range(self.size-i):
            self.ushort_p[x] = self.ushort_p[x+i]
            
    def get_text_wh(self, font):
        text_w = c_int()
        text_h = c_int()
        TTF_SizeUNICODE(font, self.ushort_p, byref(text_w), byref(text_h))
        return (text_w.value, text_h.value)
            
    def free(self):
        SDL_free(self.void_p)

if __name__ == '__main__':
    a = StrBuf("123\n123")
    a.insert("2", 0)
