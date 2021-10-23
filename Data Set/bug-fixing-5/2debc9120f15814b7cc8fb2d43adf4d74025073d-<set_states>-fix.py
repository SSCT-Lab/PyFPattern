def set_states(self, states):
    'Sets updater states.'
    self.states = pickle.loads(states)
    self.states_synced = dict.fromkeys(self.states.keys(), False)