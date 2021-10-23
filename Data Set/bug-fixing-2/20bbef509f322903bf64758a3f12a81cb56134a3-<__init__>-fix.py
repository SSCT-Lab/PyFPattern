

def __init__(self):
    self._train_epoch_size = 30000
    self._eval_epoch_size = 3000
    self._batch_size = 128
    self._num_epoch = 100
    self._learning_rate = 0.01
    self._momentum = 0.9
    self._num_label = 4
    self._seq_length = 80
    self._num_hidden = 100
    self._num_lstm_layer = 2
