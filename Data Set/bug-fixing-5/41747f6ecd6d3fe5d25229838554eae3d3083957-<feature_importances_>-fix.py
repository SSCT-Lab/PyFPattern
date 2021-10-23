@property
def feature_importances_(self):
    'Return the feature importances.\n\n        The importance of a feature is computed as the (normalized) total\n        reduction of the criterion brought by that feature.\n        It is also known as the Gini importance.\n\n        Returns\n        -------\n        feature_importances_ : ndarray of shape (n_features,)\n            Normalized total reduction of critera by feature (Gini importance).\n        '
    check_is_fitted(self)
    return self.tree_.compute_feature_importances()