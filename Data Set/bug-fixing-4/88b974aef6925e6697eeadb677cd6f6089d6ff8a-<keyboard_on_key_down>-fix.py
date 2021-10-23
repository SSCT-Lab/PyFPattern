def keyboard_on_key_down(self, window, keycode, text, modifiers):
    'The method bound to the keyboard when the instance has focus.\n\n        When the instance becomes focused, this method is bound to the\n        keyboard and will be called for every input press. The parameters are\n        the same as :meth:`kivy.core.window.WindowBase.on_key_down`.\n\n        When overwriting the method in the derived widget, super should be\n        called to enable tab cycling. If the derived widget wishes to use tab\n        for its own purposes, it can call super after it has processed the\n        character (if it does not wish to consume the tab).\n\n        Similar to other keyboard functions, it should return True if the\n        key was consumed.\n        '
    if (keycode[1] == 'tab'):
        if (['shift'] == modifiers):
            next = self.get_focus_previous()
        else:
            next = self.get_focus_next()
        if next:
            self.focus = False
            next.focus = True
        return True
    return False