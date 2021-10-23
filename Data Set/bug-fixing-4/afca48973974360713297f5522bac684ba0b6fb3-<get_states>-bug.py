def get_states(self):
    'Get updater states.'
    return pickle.dumps(self.states)