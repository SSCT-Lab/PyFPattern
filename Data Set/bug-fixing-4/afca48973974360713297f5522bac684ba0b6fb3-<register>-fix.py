@staticmethod
def register(klass):
    "Registers a new optimizer.\n\n        Once an optimizer is registered, we can create an instance of this\n        optimizer with `create_optimizer` later.\n\n        Examples\n        --------\n\n        >>> @mx.optimizer.Optimizer.register\n        ... class MyOptimizer(mx.optimizer.Optimizer):\n        ...     pass\n        >>> optim = mx.optimizer.Optimizer.create_optimizer('MyOptimizer')\n        >>> print(type(optim))\n        <class '__main__.MyOptimizer'>\n        "
    assert isinstance(klass, type)
    name = klass.__name__.lower()
    if (name in Optimizer.opt_registry):
        logging.warning('WARNING: New optimizer %s.%s is overriding existing optimizer %s.%s', klass.__module__, klass.__name__, Optimizer.opt_registry[name].__module__, Optimizer.opt_registry[name].__name__)
    Optimizer.opt_registry[name] = klass
    return klass