def __call__(self, index, grad, weight):
    'Updates weight given gradient and index.'
    if (index not in self.states):
        self.states[index] = self.optimizer.create_state(index, weight)
        self.states_synced[index] = True
    elif (not self.states_synced[index]):
        self.states[index] = self.sync_state_context(self.states[index], weight.context)
        self.states_synced[index] = True
    self.optimizer.update(index, weight, grad, self.states[index])