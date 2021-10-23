def on_touch_down(self, touch):
    if super(DropDown, self).on_touch_down(touch):
        return True
    if self.collide_point(*touch.pos):
        return True
    if (self.attach_to and self.attach_to.collide_point(*self.attach_to.to_widget(*touch.pos))):
        return True
    if self.auto_dismiss:
        self.dismiss()