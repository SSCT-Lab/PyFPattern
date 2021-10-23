

def _flow_index(self, n, batch_size=32, shuffle=False, seed=None):
    self.reset()
    while 1:
        if (seed is not None):
            np.random.seed((seed + self.total_batches_seen))
        if (self.batch_index == 0):
            index_array = np.arange(n)
            if shuffle:
                index_array = np.random.permutation(n)
        current_index = ((self.batch_index * batch_size) % n)
        if (n >= (current_index + batch_size)):
            current_batch_size = batch_size
            self.batch_index += 1
        else:
            current_batch_size = (n - current_index)
            self.batch_index = 0
        self.total_batches_seen += 1
        (yield (index_array[current_index:(current_index + current_batch_size)], current_index, current_batch_size))
