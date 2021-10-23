@observe('editing_mode')
def _editing_mode(self, change):
    u_mode = change.new.upper()
    if self.pt_app:
        self.pt_app.editing_mode = u_mode