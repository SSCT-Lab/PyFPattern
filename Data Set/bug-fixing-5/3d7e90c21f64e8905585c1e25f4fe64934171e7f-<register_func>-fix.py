def register_func(name, func):
    if (name not in __all__):
        raise ValueError('{} not a dual function.'.format(name))
    f = sys._getframe(0).f_globals
    _restore_dict[name] = f[name]
    f[name] = func