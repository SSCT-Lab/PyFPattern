def __init__(self, **kwargs):
    Logger.info('window_sdl2.py: instantiating SDL2 window')
    self._pause_loop = False
    self._win = _WindowSDL2Storage()
    super(WindowSDL, self).__init__()
    self._mouse_x = self._mouse_y = (- 1)
    self._meta_keys = (KMOD_LCTRL, KMOD_RCTRL, KMOD_RSHIFT, KMOD_LSHIFT, KMOD_RALT, KMOD_LALT, KMOD_LMETA, KMOD_RMETA)
    self.command_keys = {
        27: 'escape',
        9: 'tab',
        8: 'backspace',
        13: 'enter',
        127: 'del',
        271: 'enter',
        273: 'up',
        274: 'down',
        275: 'right',
        276: 'left',
        278: 'home',
        279: 'end',
        280: 'pgup',
        281: 'pgdown',
    }
    self._mouse_buttons_down = set()
    self.key_map = {
        SDLK_LEFT: 276,
        SDLK_RIGHT: 275,
        SDLK_UP: 273,
        SDLK_DOWN: 274,
        SDLK_HOME: 278,
        SDLK_END: 279,
        SDLK_PAGEDOWN: 281,
        SDLK_PAGEUP: 280,
        SDLK_SHIFTR: 303,
        SDLK_SHIFTL: 304,
        SDLK_SUPER: 309,
        SDLK_LCTRL: 305,
        SDLK_RCTRL: 306,
        SDLK_LALT: 308,
        SDLK_RALT: 307,
        SDLK_CAPS: 301,
        SDLK_INSERT: 277,
        SDLK_F1: 282,
        SDLK_F2: 283,
        SDLK_F3: 284,
        SDLK_F4: 285,
        SDLK_F5: 286,
        SDLK_F6: 287,
        SDLK_F7: 288,
        SDLK_F8: 289,
        SDLK_F9: 290,
        SDLK_F10: 291,
        SDLK_F11: 292,
        SDLK_F12: 293,
        SDLK_F13: 294,
        SDLK_F14: 295,
        SDLK_F15: 296,
        SDLK_KEYPADNUM: 300,
        SDLK_KP_DEVIDE: 267,
        SDLK_KP_MULTIPLY: 268,
        SDLK_KP_MINUS: 269,
        SDLK_KP_PLUS: 270,
        SDLK_KP_ENTER: 271,
        SDLK_KP_DOT: 266,
        SDLK_KP_0: 256,
        SDLK_KP_1: 257,
        SDLK_KP_2: 258,
        SDLK_KP_3: 259,
        SDLK_KP_4: 260,
        SDLK_KP_5: 261,
        SDLK_KP_6: 262,
        SDLK_KP_7: 263,
        SDLK_KP_8: 264,
        SDLK_KP_9: 265,
    }
    if (platform == 'ios'):
        self.key_map[127] = 8
    elif (platform == 'android'):
        self.key_map[1073742094] = 27
    self.bind(minimum_width=self._set_minimum_size, minimum_height=self._set_minimum_size)
    self.bind(allow_screensaver=self._set_allow_screensaver)