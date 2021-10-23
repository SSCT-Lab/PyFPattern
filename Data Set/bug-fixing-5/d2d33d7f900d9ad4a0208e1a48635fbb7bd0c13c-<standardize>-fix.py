def standardize(self, x):
    'Apply the normalization configuration to a batch of inputs.\n\n        # Arguments\n            x: batch of inputs to be normalized.\n\n        # Returns\n            The inputs, normalized.\n        '
    if self.preprocessing_function:
        x = self.preprocessing_function(x)
    if self.rescale:
        x *= self.rescale
    if self.samplewise_center:
        x -= np.mean(x, keepdims=True)
    if self.samplewise_std_normalization:
        x /= (np.std(x, keepdims=True) + 1e-07)
    if self.featurewise_center:
        if (self.mean is not None):
            x -= self.mean
        else:
            warnings.warn("This ImageDataGenerator specifies `featurewise_center`, but it hasn'tbeen fit on any training data. Fit it first by calling `.fit(numpy_data)`.")
    if self.featurewise_std_normalization:
        if (self.std is not None):
            x /= (self.std + 1e-07)
        else:
            warnings.warn("This ImageDataGenerator specifies `featurewise_std_normalization`, but it hasn'tbeen fit on any training data. Fit it first by calling `.fit(numpy_data)`.")
    if self.zca_whitening:
        if (self.principal_components is not None):
            flatx = np.reshape(x, ((- 1), np.prod(x.shape[(- 3):])))
            whitex = np.dot(flatx, self.principal_components)
            x = np.reshape(whitex, x.shape)
        else:
            warnings.warn("This ImageDataGenerator specifies `zca_whitening`, but it hasn'tbeen fit on any training data. Fit it first by calling `.fit(numpy_data)`.")
    return x