def get_end_state(self):
    'get end state info'
    bfd_dict = self.get_bfd_dict()
    if (not bfd_dict):
        return
    self.end_state['global'] = bfd_dict.get('global')
    if (self.existing == self.end_state):
        self.changed = False