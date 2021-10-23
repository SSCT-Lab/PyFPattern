def get_end_state(self):
    'get end state info'
    bfd_dict = self.get_bfd_dict()
    if (not bfd_dict):
        return
    self.end_state['session'] = bfd_dict.get('session')