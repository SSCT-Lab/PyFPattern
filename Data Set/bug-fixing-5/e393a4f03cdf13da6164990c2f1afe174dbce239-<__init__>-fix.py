def __init__(self, mode, input_size, hidden_size, num_layers=1, batch_first=False, dropout=0, train=True, bidirectional=False, batch_sizes=None, dropout_state=None, flat_weight=None):
    super(CudnnRNN, self).__init__()
    if (dropout_state is None):
        dropout_state = {
            
        }
    self.mode = cudnn.rnn.get_cudnn_mode(mode)
    self.input_mode = cudnn.CUDNN_LINEAR_INPUT
    self.input_size = input_size
    self.hidden_size = hidden_size
    self.num_layers = num_layers
    self.batch_first = batch_first
    self.dropout = dropout
    self.train = train
    self.bidirectional = (1 if bidirectional else 0)
    self.num_directions = (2 if bidirectional else 1)
    self.batch_sizes = batch_sizes
    self.dropout_seed = torch.IntTensor(1).random_()[0]
    self.dropout_state = dropout_state
    self.weight_buf = flat_weight
    if (flat_weight is None):
        warnings.warn('RNN module weights are not part of single contiguous chunk of memory. This means they need to be compacted at every call, possibly greatly increasing memory usage. To compact weights again call flatten_parameters().', stacklevel=5)