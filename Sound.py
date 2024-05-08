from ctypes import *
from sdl2 import *
from math import *
from App.Notes_info import *
from App.Color import add_in_range

from time import *

def p_add_cast(p, i, p_type):
    return cast((addressof(p.contents) + i), POINTER(p_type))

#AudioCallback

class PlayingSoundInfo(Structure):
    _fields_ = [('max_sounds', c_int), 
                ('is_playing', c_int)] 
    
class PlayingSound(Structure):
    _fields_ = [('active', c_bool),
                ('id', Uint32),
                ('buf_p', POINTER(c_float)),
                ('size', Uint32),
                ('position', Uint32),
                ('loop', c_bool)]
       
    def clear(self):
       self.active = False
       self.id = 0
       #self.buf_p = 0
       self.size = 0
       self.position = 0
       self.loop = False
       self.sinc_with_sound_id = 0
       
@CFUNCTYPE(None, c_void_p, POINTER(Uint8), c_int)
def SDL_AudioCallback_my(sounds_p, buf_p, buf_len):
    SDL_memset(buf_p, 0, buf_len)
    buf_p = cast(buf_p, POINTER(c_float))
    buf_len = int(buf_len/sizeof(c_float))
    
    info_p = cast(sounds_p, POINTER(PlayingSoundInfo))
    info = info_p.contents
    max_sounds = info.max_sounds
    sounds = p_add_cast(info_p, sizeof(PlayingSoundInfo), PlayingSound)
    sounds_to_mix = []
    for s in range(max_sounds):
        if sounds[s].active == True:
            sounds_to_mix.append(s)
            info.is_playing+=1
    
    if len(sounds_to_mix) != 0:
        info.is_playing = True
        for s in sounds_to_mix:
            if sounds[s].loop:
                for i in range(buf_len):
                    buf_p[i] += sounds[s].buf_p[sounds[s].position]
                    sounds[s].position += 1 
                    if sounds[s].position == sounds[s].size:
                        sounds[s].position = 0
            else:
                size_to_mix = sounds[s].size - sounds[s].position
                if size_to_mix > buf_len:
                    size_to_mix = buf_len
                for i in range(size_to_mix):
                    buf_p[i] += sounds[s].buf_p[sounds[s].position + i]
                if size_to_mix < buf_len:
                    sounds[s].clear()
                else:
                    sounds[s].position+=buf_len
    else:
        info.is_playing = 0
    
#Sound

def print_as(audio_spec):
    attrs = ['channels', 'freq', 'padding', 'samples', 'size', 'callback', 'userdata']
    for a in attrs:
        print('{}: {}'.format(a, getattr(audio_spec, a)))
    print('Format: ')
    print_af(audio_spec.format)
    
def print_af(num):
    print('Is signed: {}'.format((num&(1<<15))>>15))
    print('Is float: {}'.format((num&(1<<8))>>8))
    print('Sample bit size: {}'.format(num&0xFF))
    
def make_sound_dict(names, load_type, want_spec):
    result = {}
    for name in names:
        if load_type == 'wav':
            result[name] = Sound(name, load_type, Notes_files[name], want_spec)
        elif load_type == 'hz':
            result[name] = Sound(name, load_type, Notes_hz[name], want_spec)
    return result
    
class Sound:
    
    def __init__(self, name, load_type, src, want_spec, len_secs = None):
        self.name = name
        self.load_type = load_type
        if load_type == 'wav':
            self.filename = src
            self.load_wav(src, want_spec)
        elif load_type == 'hz':
            self.hz = src
            self.load_hz(src, len_secs, want_spec)
        elif load_type == 'sounds':
            self.combaine_sounds(src)
        self.bytes_per_sample = int((self.spec.format & 0xFF) / 8)
        self.frames = self.bytes_to_frames(self.size)
        self.len_secs = self.bytes_to_secs(self.size)

    def __del__(self):
        self.free_buf()

    def free_buf(self):
        SDL_free(self.buf_p)

        #sound_size_cast_funcs-------------------------------------------------
    def frames_to_bytes(self, frames):
        return frames * self.spec.channels * self.bytes_per_sample
        
    def bytes_to_frames(self, bytes_count):
        return int(bytes_count/self.spec.channels/self.bytes_per_sample)
        
    def secs_to_bytes(self, secs):
        return self.frames_to_bytes(int(secs * self.spec.freq))
        
    def bytes_to_secs(self, bytes_count):
        return self.bytes_to_frames(bytes_count)/self.spec.freq
        #-----------------------------------------------------------------------
    
    def load_wav(self, file_name, want_spec):
        self.spec = SDL_AudioSpec(0,0,0,0)
        size = c_size_t()
        temp_buf = pointer(Uint8())
        SDL_LoadWAV(file_name, byref(self.spec), byref(temp_buf), cast(byref(size), POINTER(c_ulong)))
        void_p = SDL_malloc(size)
        SDL_memcpy(void_p, temp_buf, size)
        SDL_FreeWAV(temp_buf)
        self.size = size.value
        self.buf_p = cast(void_p, POINTER(c_float))
        self.change_spec(want_spec)

    def change_spec(self, new_spec):
        cvt = SDL_AudioCVT()
        SDL_BuildAudioCVT(byref(cvt), self.spec.format, self.spec.channels, self.spec.freq, new_spec.format, new_spec.channels, new_spec.freq)
        if cvt.needed == 1:
            cvt.len = self.size
            temp_void_p = SDL_malloc(cvt.len * cvt.len_mult)
            cvt.buf = cast(temp_void_p, POINTER(Uint8))
            SDL_memcpy(cvt.buf, self.buf_p, self.size)
            self.free_buf()
            SDL_ConvertAudio(byref(cvt))
            self.size = cvt.len_cvt
            self.buf_p = cast(cvt.buf, POINTER(c_float))
            self.spec = new_spec
            return True
        else:
            return False        
        
    def load_hz(self, hz, len_secs, spec):
        self.spec = spec
        self.bytes_per_sample = int((self.spec.format & 0xFF) / 8)
        note_len_in_samples = int(self.spec.freq/hz) + 1
        if len_secs != None:
            size = self.bytes_to_samples(self.secs_to_bytes(len_secs))
            for_del = size % note_len_in_samples
            size -= for_del
            self.size = Uint32(self.samples_to_bytes(size))
        else:
            self.size = Uint32(self.samples_to_bytes(note_len_in_samples))
        self.void_p = SDL_calloc(c_size_t(self.size.value), c_size_t(1))
        self.buf = cast(self.void_p, POINTER(Uint8))
        self.samples = self.bytes_to_samples(self.size.value)
        self.make_sin_note(hz)
        
    def queue_sounds(self, sounds):
        self.spec = sounds[0].spec
        size = 0
        for i in sounds:
            size+= i.size.value
        self.size = Uint32(size)
        self.void_p = SDL_calloc(c_size_t(self.size.value), c_size_t(1))
        self.buf = cast(self.void_p, POINTER(Uint8))
        x = 0
        for i in sounds:
            SDL_memcpy(p_add_cast(self.buf, x, c_void_p), cast(i.buf, c_void_p), c_size_t(i.size.value))
            x+=i.size.value
        
    def mix_with_sound(self, sound):
        if sound.samples < self.samples:
            samples = sound.samples
        else:
            samples = self.samples
        max_value = 32767
        for i in range(samples):
            value = add_in_range(self.short_p[i*2], sound.short_p[i*2], -max_value, max_value)
            self.short_p[i*2] = value
            self.short_p[(i*2)+1] = value
        
    def mix_with_looped_sound(self, sound):
        max_value = 32767
        i_2 = 0
        for i in range(self.samples):
            if i_2 == sound.samples:
                i_2 = 0
            value = add_in_range(self.short_p[i*2], sound.short_p[i_2*2], -max_value, max_value)
            self.short_p[i*2] = value
            self.short_p[(i*2)+1] = value
            i_2+=1

    def get_slice_secs(self, start, end):
        start_p = p_add_cast(self.buf, self.secs_to_bytes(start), Uint8)
        size = Uint32(self.secs_to_bytes(end) - self.secs_to_bytes(start))
        start_p, size = self.clamp_p_size(start_p, size)
        #return size in bytes
        return start_p, size
        
    def get_slice_samples(self, start, size):
        start_p = p_add_cast(self.buf, self.samples_to_bytes(start), Uint8)
        size = Uint32(self.samples_to_bytes(size))
        start_p, size = self.clamp_p_size(start_p, size)
        #return size in bytes
        return start_p, size
    
    def get_as_points(self):
        result = []
        for i in range(self.bytes_to_frames(self.size)):
            result.append(self.buf_p[i])
        return result
        
    def clamp_p_size(self, start, size):
        end_p = p_add_cast(self.buf, self.size.value, Uint8)
        end_p_addr = addressof(end_p.contents)
        start_addr = addressof(start.contents)
        if  start_addr < addressof(self.buf.contents):
            start = self.buf
        elif start_addr > end_p_addr:
            start = end_p
            new_start_addr = addressof(start.contents)
        if new_start_addr  + size.value > end_p_addr:
            size = end_p_addr - new_start_addr
        return start, size
        
    def change(self, buf_p, samples_count):
        max_value = 32767
        short_p = cast(buf_p, POINTER(c_short))
        for i in range(samples_count):
            new_value = int(short_p[i*2]  * 1.5)
            short_p[i*2] = new_value
            short_p[(i*2)+1] = new_value
        
    def make_sin_note(self, hz):
        max_value = (32767 *0.3)
        note_len = self.spec.freq/hz
        for i in range(self.samples):
            value = int(max_value * sin(i/note_len * 2*pi))
            self.short_p[i*2] = value
            self.short_p[(i*2)+1] = value


