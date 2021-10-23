def get_config(self):
    '\n        Get the metric and current states.\n        The states are the members who do not has "_" prefix.\n\n        Args:\n            None\n\n        Returns:\n            dict: a dict of metric and states\n        '
    states = {attr: value for (attr, value) in six.iteritems(self.__dict__) if (not attr.startswith('_'))}
    config = {
        
    }
    config.update({
        'name': self._name,
        'states': copy.deepcopy(states),
    })
    return config