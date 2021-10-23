

def on_touch_down(self, touch):
    if super(ActionDropDown, self).on_touch_down(touch):
        if self.auto_dismiss:
            self.dismiss()
        return True
