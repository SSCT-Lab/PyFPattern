

def load_state_dict(self, state_dict, strict=True):
    "Copies parameters and buffers from :attr:`state_dict` into\n        this module and its descendants. If :attr:`strict` is ``True`` then\n        the keys of :attr:`state_dict` must exactly match the keys returned\n        by this module's :func:`state_dict()` function.\n\n        Arguments:\n            state_dict (dict): A dict containing parameters and\n                persistent buffers.\n            strict (bool): Strictly enforce that the keys in :attr:`state_dict`\n                match the keys returned by this module's `:func:`state_dict()`\n                function.\n        "
    own_state = self.state_dict()
    for (name, param) in state_dict.items():
        if (name in own_state):
            if isinstance(param, Parameter):
                param = param.data
            try:
                own_state[name].copy_(param)
            except Exception:
                raise RuntimeError('While copying the parameter named {}, whose dimensions in the model are {} and whose dimensions in the checkpoint are {}.'.format(name, own_state[name].size(), param.size()))
        elif strict:
            raise KeyError('unexpected key "{}" in state_dict'.format(name))
    if strict:
        missing = (set(own_state.keys()) - set(state_dict.keys()))
        if (len(missing) > 0):
            raise KeyError('missing keys in state_dict: "{}"'.format(missing))
