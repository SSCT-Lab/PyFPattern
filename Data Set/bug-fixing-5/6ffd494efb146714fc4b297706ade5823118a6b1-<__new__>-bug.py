def __new__(cls, *args, **kwargs):
    return load_platform_subclass(User, args, kwargs)