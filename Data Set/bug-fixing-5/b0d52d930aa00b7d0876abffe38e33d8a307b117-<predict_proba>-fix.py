def predict_proba(self, X, **kwargs):
    "Returns class probability estimates for the given test data.\n\n        # Arguments\n            X: array-like, shape `(n_samples, n_features)`\n                Test samples where n_samples in the number of samples\n                and n_features is the number of features.\n            kwargs: dictionary arguments\n                Legal arguments are the arguments of `Sequential.predict_classes`.\n\n        # Returns\n            proba: array-like, shape `(n_samples, n_outputs)`\n                Class probability estimates.\n                In the case of binary classification (i.e. 1 output of 0 or 1)\n                 will return '(n_samples, 2)'\n        "
    kwargs = self.filter_sk_params(Sequential.predict_proba, kwargs)
    probs = self.model.predict_proba(X, **kwargs)
    if (probs.shape[1] == 1):
        probs = numpy.hstack([(1 - probs), probs])
    return probs