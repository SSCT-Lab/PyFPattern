@observe('editing_mode')
def _editing_mode(self, change):
    u_mode = change.new.upper()
    self.pt_app.editing_mode = u_mode