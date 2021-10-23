def restore_func(name):
    if (name not in __all__):
        raise ValueError('{} not a dual function.'.format(name))
    try:
        val = _restore_dict[name]
    except KeyError:
        return
    else:
        sys._getframe(0).f_globals[name] = val