def state_dict(self, destination=None, prefix='', keep_vars=False):
    "Returns a dictionary containing a whole state of the module.\n\n        Both parameters and persistent buffers (e.g. running averages) are\n        included. Keys are corresponding parameter and buffer names.\n\n        When keep_vars is ``True``, it returns a Variable for each parameter\n        (rather than a Tensor).\n\n        Args:\n            destination (dict, optional):\n                if not None, the return dictionary is stored into destination.\n                Default: None\n            prefix (string, optional): Adds a prefix to the key (name) of every\n                parameter and buffer in the result dictionary. Default: ''\n            keep_vars (bool, optional): if ``True``, returns a Variable for each\n                parameter. If ``False``, returns a Tensor for each parameter.\n                Default: ``False``\n\n        Returns:\n            dict:\n                a dictionary containing a whole state of the module\n\n        Example::\n\n            >>> module.state_dict().keys()\n            ['bias', 'weight']\n\n        "
    if (destination is None):
        destination = OrderedDict()
    for (name, param) in self._parameters.items():
        if (param is not None):
            destination[(prefix + name)] = (param if keep_vars else param.data)
    for (name, buf) in self._buffers.items():
        if (buf is not None):
            destination[(prefix + name)] = buf
    for (name, module) in self._modules.items():
        if (module is not None):
            module.state_dict(destination, ((prefix + name) + '.'), keep_vars=keep_vars)
    return destination