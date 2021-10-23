def AutogradRNN(mode, input_size, hidden_size, num_layers=1, batch_first=False, dropout=0, train=True, bidirectional=False):
    if (mode == 'RNN_RELU'):
        cell = RNNReLUCell
    elif (mode == 'RNN_TANH'):
        cell = RNNTanhCell
    elif (mode == 'LSTM'):
        cell = LSTMCell
    elif (mode == 'GRU'):
        cell = GRUCell
    else:
        raise Exception('Unknown mode: {}'.format(mode))
    if bidirectional:
        layer = (Recurrent(cell), Recurrent(cell, reverse=True))
    else:
        layer = (Recurrent(cell),)
    func = StackedRNN(layer, num_layers, (mode == 'LSTM'), dropout=dropout, train=train)

    def forward(input, weight, hidden):
        if batch_first:
            input.transpose(0, 1)
        (nexth, output) = func(input, hidden, weight)
        if batch_first:
            output.transpose(0, 1)
        return (output, nexth)
    return forward