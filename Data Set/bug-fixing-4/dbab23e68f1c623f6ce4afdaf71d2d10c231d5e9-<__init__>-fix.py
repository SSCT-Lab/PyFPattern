def __init__(self, *args, **kwargs):
    super(CallbackModule, self).__init__(*args, **kwargs)
    self.task = None
    self.play = None