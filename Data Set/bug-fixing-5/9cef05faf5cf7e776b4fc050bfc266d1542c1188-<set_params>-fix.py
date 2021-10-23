def set_params(self, **params):
    "Set the parameters of this estimator.\n\n        The method works on simple estimators as well as on nested objects\n        (such as pipelines). The latter have parameters of the form\n        ``<component>__<parameter>`` so that it's possible to update each\n        component of a nested object.\n\n        Returns\n        -------\n        self\n        "
    if (not params):
        return self
    valid_params = self.get_params(deep=True)
    for (key, value) in six.iteritems(params):
        split = key.split('__', 1)
        if (len(split) > 1):
            (name, sub_name) = split
            if (name not in valid_params):
                raise ValueError(('Invalid parameter %s for estimator %s. Check the list of available parameters with `estimator.get_params().keys()`.' % (name, self)))
            sub_object = valid_params[name]
            sub_object.set_params(**{
                sub_name: value,
            })
        else:
            if (key not in valid_params):
                raise ValueError(('Invalid parameter %s for estimator %s. Check the list of available parameters with `estimator.get_params().keys()`.' % (key, self.__class__.__name__)))
            setattr(self, key, value)
    return self