

def _mainloop(self):
    EventLoop.idle()
    while self._pause_loop:
        self._win.wait_event()
        if (not self._pause_loop):
            break
        self._win.poll()
    while True:
        event = self._win.poll()
        if (event is False):
            break
        if (event is None):
            continue
        (action, args) = (event[0], event[1:])
        if (action == 'quit'):
            if self.dispatch('on_request_close'):
                continue
            EventLoop.quit = True
            self.close()
            break
        elif (action in ('fingermotion', 'fingerdown', 'fingerup')):
            if (platform in ('ios', 'android')):
                SDL2MotionEventProvider.q.appendleft(event)
            pass
        elif (action == 'mousemotion'):
            (x, y) = args
            (x, y) = self._fix_mouse_pos(x, y)
            self._mouse_x = x
            self._mouse_y = y
            if (len(self._mouse_buttons_down) == 0):
                continue
            self._mouse_meta = self.modifiers
            self.dispatch('on_mouse_move', x, y, self.modifiers)
        elif (action in ('mousebuttondown', 'mousebuttonup')):
            (x, y, button) = args
            (x, y) = self._fix_mouse_pos(x, y)
            btn = 'left'
            if (button == 3):
                btn = 'right'
            elif (button == 2):
                btn = 'middle'
            eventname = 'on_mouse_down'
            self._mouse_buttons_down.add(button)
            if (action == 'mousebuttonup'):
                eventname = 'on_mouse_up'
                self._mouse_buttons_down.remove(button)
            self._mouse_x = x
            self._mouse_y = y
            self.dispatch(eventname, x, y, btn, self.modifiers)
        elif action.startswith('mousewheel'):
            self._update_modifiers()
            (x, y, button) = args
            btn = 'scrolldown'
            if action.endswith('up'):
                btn = 'scrollup'
            elif action.endswith('right'):
                btn = 'scrollright'
            elif action.endswith('left'):
                btn = 'scrollleft'
            self._mouse_meta = self.modifiers
            self._mouse_btn = btn
            self._mouse_down = True
            self.dispatch('on_mouse_down', self._mouse_x, self._mouse_y, btn, self.modifiers)
            self._mouse_down = False
            self.dispatch('on_mouse_up', self._mouse_x, self._mouse_y, btn, self.modifiers)
        elif (action == 'dropfile'):
            dropfile = args
            self.dispatch('on_dropfile', dropfile[0])
        elif (action == 'windowresized'):
            self._size = self._win.window_size
            ev = self._do_resize_ev
            if (ev is None):
                ev = Clock.schedule_once(self._do_resize, 0.1)
                self._do_resize_ev = ev
            else:
                ev()
        elif (action == 'windowresized'):
            self.canvas.ask_update()
        elif (action == 'windowrestored'):
            self.dispatch('on_restore')
            self.canvas.ask_update()
        elif (action == 'windowexposed'):
            self.canvas.ask_update()
        elif (action == 'windowminimized'):
            self.dispatch('on_minimize')
            if Config.getboolean('kivy', 'pause_on_minimize'):
                self.do_pause()
        elif (action == 'windowmaximized'):
            self.dispatch('on_maximize')
        elif (action == 'windowhidden'):
            self.dispatch('on_hide')
        elif (action == 'windowshown'):
            self.dispatch('on_show')
        elif (action == 'windowfocusgained'):
            self._focus = True
        elif (action == 'windowfocuslost'):
            self._focus = False
        elif (action == 'windowenter'):
            self.dispatch('on_cursor_enter')
        elif (action == 'windowleave'):
            self.dispatch('on_cursor_leave')
        elif (action == 'joyaxismotion'):
            (stickid, axisid, value) = args
            self.dispatch('on_joy_axis', stickid, axisid, value)
        elif (action == 'joyhatmotion'):
            (stickid, hatid, value) = args
            self.dispatch('on_joy_hat', stickid, hatid, value)
        elif (action == 'joyballmotion'):
            (stickid, ballid, xrel, yrel) = args
            self.dispatch('on_joy_ball', stickid, ballid, xrel, yrel)
        elif (action == 'joybuttondown'):
            (stickid, buttonid) = args
            self.dispatch('on_joy_button_down', stickid, buttonid)
        elif (action == 'joybuttonup'):
            (stickid, buttonid) = args
            self.dispatch('on_joy_button_up', stickid, buttonid)
        elif (action in ('keydown', 'keyup')):
            (mod, key, scancode, kstr) = args
            try:
                key = self.key_map[key]
            except KeyError:
                pass
            if (action == 'keydown'):
                self._update_modifiers(mod, key)
            else:
                self._update_modifiers(mod)
            if ((key not in self._modifiers) and (key not in self.command_keys.keys())):
                try:
                    kstr_chr = unichr(key)
                    try:
                        encoding = (getattr(sys.stdout, 'encoding', 'utf8') or 'utf8')
                        kstr_chr.encode(encoding)
                        kstr = kstr_chr
                    except UnicodeError:
                        pass
                except ValueError:
                    pass
            if (action == 'keyup'):
                self.dispatch('on_key_up', key, scancode)
                continue
            if self.dispatch('on_key_down', key, scancode, kstr, self.modifiers):
                continue
            self.dispatch('on_keyboard', key, scancode, kstr, self.modifiers)
        elif (action == 'textinput'):
            text = args[0]
            self.dispatch('on_textinput', text)
        else:
            Logger.trace(('WindowSDL: Unhandled event %s' % str(event)))
