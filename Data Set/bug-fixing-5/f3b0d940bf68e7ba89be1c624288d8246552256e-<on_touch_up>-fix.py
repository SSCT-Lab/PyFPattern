def on_touch_up(self, touch):
    if ((self._touch is not touch) and (self._get_uid() not in touch.ud)):
        touch.push()
        touch.apply_transform_2d(self.to_local)
        if super(ScrollView, self).on_touch_up(touch):
            touch.pop()
            return True
        touch.pop()
        return False
    if self.dispatch('on_scroll_stop', touch):
        touch.ungrab(self)
        if (not touch.ud.get('sv.can_defocus', True)):
            FocusBehavior.ignored_touch.append(touch)
        return True