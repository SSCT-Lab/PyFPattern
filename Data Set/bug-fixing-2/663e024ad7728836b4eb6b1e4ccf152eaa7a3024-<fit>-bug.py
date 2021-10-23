

def fit(self, X, y):
    '\n        Fit the NearestCentroid model according to the given training data.\n\n        Parameters\n        ----------\n        X : {array-like, sparse matrix}, shape = [n_samples, n_features]\n            Training vector, where n_samples in the number of samples and\n            n_features is the number of features.\n            Note that centroid shrinking cannot be used with sparse matrices.\n        y : array, shape = [n_samples]\n            Target values (integers)\n        '
    if (self.metric == 'precomputed'):
        raise ValueError('Precomputed is not supported.')
    if (self.metric == 'manhattan'):
        (X, y) = check_X_y(X, y, ['csc'])
    else:
        (X, y) = check_X_y(X, y, ['csr', 'csc'])
    is_X_sparse = sp.issparse(X)
    if (is_X_sparse and self.shrink_threshold):
        raise ValueError('threshold shrinking not supported for sparse input')
    check_classification_targets(y)
    (n_samples, n_features) = X.shape
    le = LabelEncoder()
    y_ind = le.fit_transform(y)
    self.classes_ = classes = le.classes_
    n_classes = classes.size
    if (n_classes < 2):
        raise ValueError(('The number of classes has to be greater than one; got %d class' % n_classes))
    self.centroids_ = np.empty((n_classes, n_features), dtype=np.float64)
    nk = np.zeros(n_classes)
    for cur_class in range(n_classes):
        center_mask = (y_ind == cur_class)
        nk[cur_class] = np.sum(center_mask)
        if is_X_sparse:
            center_mask = np.where(center_mask)[0]
        if (self.metric == 'manhattan'):
            if (not is_X_sparse):
                self.centroids_[cur_class] = np.median(X[center_mask], axis=0)
            else:
                self.centroids_[cur_class] = csc_median_axis_0(X[center_mask])
        else:
            if (self.metric != 'euclidean'):
                warnings.warn('Averaging for metrics other than euclidean and manhattan not supported. The average is set to be the mean.')
            self.centroids_[cur_class] = X[center_mask].mean(axis=0)
    if self.shrink_threshold:
        dataset_centroid_ = np.mean(X, axis=0)
        m = np.sqrt(((1.0 / nk) - (1.0 / n_samples)))
        variance = ((X - self.centroids_[y_ind]) ** 2)
        variance = variance.sum(axis=0)
        s = np.sqrt((variance / (n_samples - n_classes)))
        s += np.median(s)
        mm = m.reshape(len(m), 1)
        ms = (mm * s)
        deviation = ((self.centroids_ - dataset_centroid_) / ms)
        signs = np.sign(deviation)
        deviation = (np.abs(deviation) - self.shrink_threshold)
        np.clip(deviation, 0, None, out=deviation)
        deviation *= signs
        msd = (ms * deviation)
        self.centroids_ = (dataset_centroid_[np.newaxis, :] + msd)
    return self
