def get_config(self):
    '\n        Get the metric and current states.\n        The states are the members who do not has "_" prefix.\n\n        Args:\n            None\n\n        Returns:\n            a python dict, which costains the inner states of the metric instance\n\n        Return types:\n            a python dict\n        '
    states = {attr: value for (attr, value) in six.iteritems(self.__dict__) if (not attr.startswith('_'))}
    config = {
        
    }
    config.update({
        'name': self._name,
        'states': copy.deepcopy(states),
    })
    return config