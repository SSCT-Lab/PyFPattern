@property
def predict_proba(self):
    'Probability estimates.\n\n        This method is only available for log loss and modified Huber loss.\n\n        Multiclass probability estimates are derived from binary (one-vs.-rest)\n        estimates by simple normalization, as recommended by Zadrozny and\n        Elkan.\n\n        Binary probability estimates for loss="modified_huber" are given by\n        (clip(decision_function(X), -1, 1) + 1) / 2. For other loss functions\n        it is necessary to perform proper probability calibration by wrapping\n        the classifier with\n        :class:`sklearn.calibration.CalibratedClassifierCV` instead.\n\n        Parameters\n        ----------\n        X : {array-like, sparse matrix}, shape (n_samples, n_features)\n            Input data for prediction.\n\n        Returns\n        -------\n        array, shape (n_samples, n_classes)\n            Returns the probability of the sample for each class in the model,\n            where classes are ordered as they are in `self.classes_`.\n\n        References\n        ----------\n        Zadrozny and Elkan, "Transforming classifier scores into multiclass\n        probability estimates", SIGKDD\'02,\n        http://www.research.ibm.com/people/z/zadrozny/kdd2002-Transf.pdf\n\n        The justification for the formula in the loss="modified_huber"\n        case is in the appendix B in:\n        http://jmlr.csail.mit.edu/papers/volume2/zhang02c/zhang02c.pdf\n        '
    self._check_proba()
    return self._predict_proba