def _flow_index(self, N, batch_size=32, shuffle=False, seed=None):
    while 1:
        index_array = np.arange(N)
        if (self.batch_index == 0):
            if shuffle:
                if (seed is not None):
                    np.random.seed((seed + self.total_batches_seen))
                index_array = np.random.permutation(N)
        current_index = ((self.batch_index * batch_size) % N)
        if (N >= (current_index + batch_size)):
            current_batch_size = batch_size
            self.batch_index += 1
        else:
            current_batch_size = (N - current_index)
            self.batch_index = 0
        self.total_batches_seen += 1
        (yield (index_array[current_index:(current_index + current_batch_size)], current_index, current_batch_size))