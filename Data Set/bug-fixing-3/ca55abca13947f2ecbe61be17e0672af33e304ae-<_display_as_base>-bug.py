def _display_as_base(cls):
    '\n    A decorator that makes an exception class look like its base.\n\n    We use this to hide subclasses that are implementation details - the user\n    should catch the base type, which is what the traceback will show them.\n\n    Classes decorated with this decorator are subject to removal without a\n    deprecation warning.\n    '
    assert issubclass(cls, Exception)
    cls.__name__ = cls.__base__.__name__
    cls.__qualname__ = cls.__base__.__qualname__
    return cls