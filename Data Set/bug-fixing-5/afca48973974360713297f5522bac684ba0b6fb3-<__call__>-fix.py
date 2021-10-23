def __call__(self, index, grad, weight):
    'Updates weight given gradient and index.'
    if (index not in self.states):
        self.states[index] = self.optimizer.create_state(index, weight)
    self.optimizer.update(index, weight, grad, self.states[index])