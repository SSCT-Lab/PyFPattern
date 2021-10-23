

def create_instance(objcls, settings, crawler, *args, **kwargs):
    'Construct a class instance using its ``from_crawler`` or\n    ``from_settings`` constructors, if available.\n\n    At least one of ``settings`` and ``crawler`` needs to be different from\n    ``None``. If ``settings `` is ``None``, ``crawler.settings`` will be used.\n    If ``crawler`` is ``None``, only the ``from_settings`` constructor will be\n    tried.\n\n    ``*args`` and ``**kwargs`` are forwarded to the constructors.\n\n    Raises ``ValueError`` if both ``settings`` and ``crawler`` are ``None``.\n    '
    if (settings is None):
        if (crawler is None):
            raise ValueError('Specifiy at least one of settings and crawler.')
        settings = crawler.settings
    if (crawler and hasattr(objcls, 'from_crawler')):
        return objcls.from_crawler(crawler, *args, **kwargs)
    elif hasattr(objcls, 'from_settings'):
        return objcls.from_settings(settings, *args, **kwargs)
    else:
        return objcls(*args, **kwargs)
