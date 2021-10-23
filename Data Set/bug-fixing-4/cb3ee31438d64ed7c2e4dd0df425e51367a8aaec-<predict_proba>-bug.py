def predict_proba(self, x, **kwargs):
    "Returns class probability estimates for the given test data.\n\n        # Arguments\n            x: array-like, shape `(n_samples, n_features)`\n                Test samples where n_samples in the number of samples\n                and n_features is the number of features.\n            **kwargs: dictionary arguments\n                Legal arguments are the arguments\n                of `Sequential.predict_classes`.\n\n        # Returns\n            proba: array-like, shape `(n_samples, n_outputs)`\n                Class probability estimates.\n                In the case of binary classification,\n                tp match the scikit-learn API,\n                will return an array of shape '(n_samples, 2)'\n                (instead of `(n_sample, 1)` as in Keras).\n        "
    kwargs = self.filter_sk_params(Sequential.predict_proba, kwargs)
    probs = self.model.predict_proba(x, **kwargs)
    if (probs.shape[1] == 1):
        probs = np.hstack([(1 - probs), probs])
    return probs