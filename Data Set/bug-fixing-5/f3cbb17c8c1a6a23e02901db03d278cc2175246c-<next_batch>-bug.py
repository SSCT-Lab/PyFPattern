def next_batch(self, batch_size, fake_data=False):
    'Return the next `batch_size` examples from this data set.'
    if fake_data:
        fake_image = ([1] * 784)
        if self.one_hot:
            fake_label = ([1] + ([0] * 9))
        else:
            fake_label = 0
        return ([fake_image for _ in xrange(batch_size)], [fake_label for _ in xrange(batch_size)])
    start = self._index_in_epoch
    self._index_in_epoch += batch_size
    if (self._index_in_epoch > self._num_examples):
        self._epochs_completed += 1
        perm = numpy.arange(self._num_examples)
        numpy.random.shuffle(perm)
        self._images = self._images[perm]
        self._labels = self._labels[perm]
        start = 0
        self._index_in_epoch = batch_size
        assert (batch_size <= self._num_examples)
    end = self._index_in_epoch
    return (self._images[start:end], self._labels[start:end])