def check_forward_args(self, input, hidden, batch_sizes):
    is_input_packed = (batch_sizes is not None)
    expected_input_dim = (2 if is_input_packed else 3)
    if (input.dim() != expected_input_dim):
        raise RuntimeError('input must have {} dimensions, got {}'.format(expected_input_dim, input.dim()))
    if (self.input_size != input.size((- 1))):
        raise RuntimeError('input.size(-1) must be equal to input_size. Expected {}, got {}'.format(fn.input_size, input.size((- 1))))
    if is_input_packed:
        mini_batch = batch_sizes[0]
    else:
        mini_batch = (input.size(0) if self.batch_first else input.size(1))
    num_directions = (2 if self.bidirectional else 1)
    expected_hidden_size = ((self.num_layers * num_directions), mini_batch, self.hidden_size)

    def check_hidden_size(hx, expected_hidden_size, msg='Expected hidden size {}, got {}'):
        if (tuple(hx.size()) != expected_hidden_size):
            raise RuntimeError(msg.format(expected_hidden_size, tuple(hx.size())))
    if (self.mode == 'LSTM'):
        check_hidden_size(hidden[0], expected_hidden_size, 'Expected hidden[0] size {}, got {}')
        check_hidden_size(hidden[1], expected_hidden_size, 'Expected hidden[1] size {}, got {}')
    else:
        check_hidden_size(hidden, expected_hidden_size)