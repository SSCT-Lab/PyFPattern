

def check_forward_hidden(self, input, hx, hidden_label=''):
    if (input.size(0) != hx.size(0)):
        raise RuntimeError("Input batch size {} doesn't match hidden{} batch size {}".format(input.size(0), hidden_label, hx.size(0)))
    if (hx.size(1) != self.hidden_size):
        raise RuntimeError('hidden{} has inconsistent hidden_size: got {}, expected {}'.format(hidden_label, hx.size(1), self.hidden_size))
