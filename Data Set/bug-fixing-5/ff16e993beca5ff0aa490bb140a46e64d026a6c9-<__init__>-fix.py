def __init__(self):
    self.super_ref = super(CallbackModule, self)
    self.super_ref.__init__()
    self.last_task = None
    self.last_task_banner = None
    self.shown_title = False