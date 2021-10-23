def on_touch_down(self, touch):
    if (self.collide_point(*touch.pos) and touch.is_double_tap):
        self.edit()
        return True
    return super(MutableTextInput, self).on_touch_down(touch)