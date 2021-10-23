def get_states(self):
    'Gets updater states.'
    return pickle.dumps(self.states)