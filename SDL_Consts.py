def get_name_by_value(dict, value):
    return list(dict.keys())[list(dict.values()).index(value)]
    
SDL_Events = {
"SDL_FIRSTEVENT" : 0,
"SDL_QUIT" : 0x100,
"SDL_APP_TERMINATING" : 0x101,
"SDL_APP_LOWMEMORY" : 0x102,
"SDL_APP_WILLENTERBACKGROUND" : 0x103,
"SDL_APP_DIDENTERBACKGROUND" : 0x104,
"SDL_APP_WILLENTERFOREGROUND" : 0x105,
"SDL_APP_DIDENTERFOREGROUND" : 0x106,
"SDL_DISPLAYEVENT" : 0x150,
"SDL_WINDOWEVENT" : 0x200,
"SDL_SYSWMEVENT" : 0x201,
"SDL_KEYDOWN" : 0x300,
"SDL_KEYUP" : 0x301,
"SDL_TEXTEDITING" : 0x302,
"SDL_TEXTINPUT" : 0x303,
"SDL_KEYMAPCHANGED" : 0x304,
"SDL_MOUSEMOTION" : 0x400,
"SDL_MOUSEBUTTONDOWN" : 0x401,
"SDL_MOUSEBUTTONUP" : 0x402,
"SDL_MOUSEWHEEL" : 0x403,
"SDL_JOYAXISMOTION" : 0x600,
"SDL_JOYBALLMOTION" : 0x601,
"SDL_JOYHATMOTION" : 0x602,
"SDL_JOYBUTTONDOWN" : 0x603,
"SDL_JOYBUTTONUP" : 0x604,
"SDL_JOYDEVICEADDED" : 0x605,
"SDL_JOYDEVICEREMOVED" : 0x606,
"SDL_CONTROLLERAXISMOTION" : 0x650,
"SDL_CONTROLLERBUTTONDOWN" : 0x651,
"SDL_CONTROLLERBUTTONUP" : 0x652,
"SDL_CONTROLLERDEVICEADDED" : 0x653,
"SDL_CONTROLLERDEVICEREMOVED" : 0x654,
"SDL_CONTROLLERDEVICEREMAPPED" : 0x655,
"SDL_FINGERDOWN" : 0x700,
"SDL_FINGERUP" : 0x701,
"SDL_FINGERMOTION" : 0x702,
"SDL_DOLLARGESTURE" : 0x800,
"SDL_DOLLARRECORD" : 0x801,
"SDL_MULTIGESTURE" : 0x802,
"SDL_CLIPBOARDUPDATE" : 0x900,
"SDL_DROPFILE" : 0x1000,
"SDL_DROPTEXT" : 0x1001,
"SDL_DROPBEGIN" : 0x1002,
"SDL_DROPCOMPLETE" : 0x1003,
"SDL_AUDIODEVICEADDED" : 0x1100,
"SDL_AUDIODEVICEREMOVED" : 0x1101,
"SDL_SENSORUPDATE" : 0x1200,
"SDL_RENDER_TARGETS_RESET" : 0x2000,
"SDL_RENDER_DEVICE_RESET" : 0x2001,
"SDL_USEREVENT" : 0x8000,
"SDL_LASTEVENT" : 0xFFFF
}

SDL_to_app_events = {
"SDL_QUIT" : "END" 
}

SDL_Window_Event_type = '''None
Shown
Hidden
Exposed
Moved
Resized
SizeChanged
Minimized
Maximized
Restored
Enter
Leave
FocusGained
FocusLost
Close'''

SDL_Pixel_Types = {
"SDL_PF_index8" : (1<<28)|(3<<24)|(8<<8)|(1<<0),
"SDL_PF_argb8888" : ((1 << 28)|((6) << 24)|((3) << 20)|((6) << 16)|((32) << 8)|((4) << 0))
}
