def _make_validation_split(self, y):
    'Split the dataset between training set and validation set.\n\n        Parameters\n        ----------\n        y : array, shape (n_samples, )\n            Target values.\n\n        Returns\n        -------\n        validation_mask : array, shape (n_samples, )\n            Equal to 1 on the validation set, 0 on the training set.\n        '
    n_samples = y.shape[0]
    validation_mask = np.zeros(n_samples, dtype=np.uint8)
    if (not self.early_stopping):
        return validation_mask
    if is_classifier(self):
        splitter_type = StratifiedShuffleSplit
    else:
        splitter_type = ShuffleSplit
    cv = splitter_type(test_size=self.validation_fraction, random_state=self.random_state)
    (idx_train, idx_val) = next(cv.split(np.zeros(shape=(y.shape[0], 1)), y))
    if ((idx_train.shape[0] == 0) or (idx_val.shape[0] == 0)):
        raise ValueError(('Splitting %d samples into a train set and a validation set with validation_fraction=%r led to an empty set (%d and %d samples). Please either change validation_fraction, increase number of samples, or disable early_stopping.' % (n_samples, self.validation_fraction, idx_train.shape[0], idx_val.shape[0])))
    validation_mask[idx_val] = 1
    return validation_mask