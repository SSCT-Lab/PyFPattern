def add_methods(cls, new_methods, force, select, exclude):
    if (select and exclude):
        raise TypeError('May only pass either select or exclude')
    if select:
        select = set(select)
        methods = {
            
        }
        for (key, method) in new_methods.items():
            if (key in select):
                methods[key] = method
        new_methods = methods
    if exclude:
        for k in exclude:
            new_methods.pop(k, None)
    for (name, method) in new_methods.items():
        if (force or (name not in cls.__dict__)):
            bind_method(cls, name, method)