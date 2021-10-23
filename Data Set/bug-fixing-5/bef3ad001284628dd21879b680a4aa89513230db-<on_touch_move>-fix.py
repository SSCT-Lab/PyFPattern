def on_touch_move(self, touch):
    if (self._touch is not touch):
        if self.collide_point(*touch.pos):
            touch.push()
            touch.apply_transform_2d(self.to_local)
            super(ScrollView, self).on_touch_move(touch)
            touch.pop()
        return (self._get_uid() in touch.ud)
    if (touch.grab_current is not self):
        return True
    if (not any(((isinstance(key, str) and key.startswith('sv.')) for key in touch.ud))):
        if self.collide_point(*touch.pos):
            touch.push()
            touch.apply_transform_2d(self.to_local)
            res = super(ScrollView, self).on_touch_move(touch)
            touch.pop()
            return res
        return False
    touch.ud['sv.handled'] = {
        'x': False,
        'y': False,
    }
    if self.dispatch('on_scroll_move', touch):
        return True