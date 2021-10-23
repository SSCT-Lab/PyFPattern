def next_batch(self, batch_size, fake_data=False, shuffle=True):
    'Return the next `batch_size` examples from this data set.'
    if fake_data:
        fake_image = ([1] * 784)
        if self.one_hot:
            fake_label = ([1] + ([0] * 9))
        else:
            fake_label = 0
        return ([fake_image for _ in xrange(batch_size)], [fake_label for _ in xrange(batch_size)])
    start = self._index_in_epoch
    if ((self._epochs_completed == 0) and (start == 0) and shuffle):
        perm0 = numpy.arange(self._num_examples)
        numpy.random.shuffle(perm0)
        self._images = self.images[perm0]
        self._labels = self.labels[perm0]
    if ((start + batch_size) > self._num_examples):
        self._epochs_completed += 1
        rest_num_examples = (self._num_examples - start)
        images_rest_part = self._images[start:self._num_examples]
        labels_rest_part = self._labels[start:self._num_examples]
        if shuffle:
            perm = numpy.arange(self._num_examples)
            numpy.random.shuffle(perm)
            self._images = self.images[perm]
            self._labels = self.labels[perm]
        start = 0
        self._index_in_epoch = (batch_size - rest_num_examples)
        end = self._index_in_epoch
        images_new_part = self.images[start:end]
        labels_new_part = self.labels[start:end]
        return (numpy.concatenate((images_rest_part, images_new_part), axis=0), numpy.concatenate((labels_rest_part, labels_new_part), axis=0))
    else:
        self._index_in_epoch += batch_size
        end = self._index_in_epoch
        return (self._images[start:end], self._labels[start:end])