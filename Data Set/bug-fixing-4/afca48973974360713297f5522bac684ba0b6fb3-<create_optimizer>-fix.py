@staticmethod
def create_optimizer(name, **kwargs):
    "Instantiates an optimizer with a given name and kwargs.\n\n        .. note:: We can use the alias `create` for ``Optimizer.create_optimizer``.\n\n        Parameters\n        ----------\n        name: str\n            Name of the optimizer. Should be the name\n            of a subclass of Optimizer. Case insensitive.\n\n        kwargs: dict\n            Parameters for the optimizer.\n\n        Returns\n        -------\n        Optimizer\n            An instantiated optimizer.\n\n        Examples\n        --------\n        >>> sgd = mx.optimizer.Optimizer.create_optimizer('sgd')\n        >>> type(sgd)\n        <class 'mxnet.optimizer.SGD'>\n        >>> adam = mx.optimizer.create('adam', learning_rate=.1)\n        >>> type(adam)\n        <class 'mxnet.optimizer.Adam'>\n        "
    if (name.lower() in Optimizer.opt_registry):
        return Optimizer.opt_registry[name.lower()](**kwargs)
    else:
        raise ValueError(('Cannot find optimizer %s' % name))