def load_state_dict(self, state_dict):
    "Copies parameters and buffers from :attr:`state_dict` into\n        this module and its descendants. The keys of :attr:`state_dict` must\n        exactly match the keys returned by this module's :func:`state_dict()`\n        function.\n\n        Arguments:\n            state_dict (dict): A dict containing parameters and\n                persistent buffers.\n        "
    own_state = self.state_dict()
    for (name, param) in state_dict.items():
        if (name not in own_state):
            raise KeyError('unexpected key "{}" in state_dict'.format(name))
        if isinstance(param, Parameter):
            param = param.data
        own_state[name].copy_(param)
    missing = (set(own_state.keys()) - set(state_dict.keys()))
    if (len(missing) > 0):
        raise KeyError('missing keys in state_dict: "{}"'.format(missing))