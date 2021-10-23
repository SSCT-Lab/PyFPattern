def reset_states(self, states=None):
    if (not self.stateful):
        raise AttributeError('Layer must be stateful.')
    batch_size = self.input_spec[0].shape[0]
    if (not batch_size):
        raise ValueError('If a RNN is stateful, it needs to know its batch size. Specify the batch size of your input tensors: \n- If using a Sequential model, specify the batch size by passing a `batch_input_shape` argument to your first layer.\n- If using the functional API, specify the time dimension by passing a `batch_shape` argument to your Input layer.')
    if (self.states[0] is None):
        if hasattr(self.cell.state_size, '__len__'):
            self.states = [K.zeros((batch_size, dim)) for dim in self.cell.state_size]
        else:
            self.states = [K.zeros((batch_size, self.cell.state_size))]
    elif (states is None):
        if hasattr(self.cell.state_size, '__len__'):
            for (state, dim) in zip(self.states, self.cell.state_size):
                K.set_value(state, np.zeros((batch_size, dim)))
        else:
            K.set_value(self.states[0], np.zeros((batch_size, self.cell.state_size)))
    else:
        if (not isinstance(states, (list, tuple))):
            states = [states]
        if (len(states) != len(self.states)):
            raise ValueError(((((((('Layer ' + self.name) + ' expects ') + str(len(self.states))) + ' states, but it received ') + str(len(states))) + ' state values. Input received: ') + str(states)))
        for (index, (value, state)) in enumerate(zip(states, self.states)):
            if hasattr(self.cell.state_size, '__len__'):
                dim = self.cell.state_size[index]
            else:
                dim = self.cell.state_size
            if (value.shape != (batch_size, dim)):
                raise ValueError(((((((('State ' + str(index)) + ' is incompatible with layer ') + self.name) + ': expected shape=') + str((batch_size, dim))) + ', found shape=') + str(value.shape)))
            K.set_value(state, value)