def restore_func(name):
    if (name not in __all__):
        raise ValueError(('%s not a dual function.' % name))
    try:
        val = _restore_dict[name]
    except KeyError:
        return
    else:
        sys._getframe(0).f_globals[name] = val