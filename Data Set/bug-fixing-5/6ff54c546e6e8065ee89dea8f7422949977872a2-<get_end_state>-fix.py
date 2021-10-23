def get_end_state(self):
    'get end state info'
    if (not self.startup_info):
        self.end_state['StartupInfos'] = None
    else:
        self.end_state['StartupInfos'] = self.startup_info['StartupInfos']
    if (self.end_state == self.existing):
        self.changed = False