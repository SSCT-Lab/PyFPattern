

def get_constant(self, name, value=None):
    'Retrieves a :py:class:`Constant` with name ``self.prefix+name``. If not found,\n        :py:func:`get` will first try to retrieve it from "shared" dict. If still not\n        found, :py:func:`get` will create a new :py:class:`Constant` with key-word\n        arguments and insert it to self.\n\n        Parameters\n        ----------\n        name : str\n            Name of the desired Constant. It will be prepended with this dictionary\'s\n            prefix.\n        value : array-like\n            Initial value of constant.\n\n        Returns\n        -------\n        Constant\n            The created or retrieved :py:class:`Constant`.\n        '
    name = (self.prefix + name)
    param = self._get_impl(name)
    if (param is None):
        if (value is None):
            raise KeyError("No constant named '{}'. Please specify value if you want to create a new constant.".format(name))
        param = Constant(name, value)
        self._params[name] = param
    elif (value is not None):
        assert isinstance(param, Constant), "Parameter '{}' already exists but it is not a constant.".format(name)
        if isinstance(value, ndarray.NDArray):
            value = value.asnumpy()
        assert ((param.shape == value.shape) and (param.value.asnumpy() == value).all()), "Constant '{}' already exists but it's value doesn't match new value".format(name)
    return param
