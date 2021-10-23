def linkcode_resolve(domain, info):
    if ((domain != 'py') or (not info['module'])):
        return None
    rtd_version = os.environ.get('READTHEDOCS_VERSION')
    if (rtd_version == 'latest'):
        tag = 'master'
    else:
        tag = 'v{}'.format(__version__)
    obj = _import_object_from_name(info['module'], info['fullname'])
    mod = inspect.getmodule(obj)
    if (mod is None):
        return None
    if (not ((mod.__name__ == 'chainer') or mod.__name__.startswith('chainer.'))):
        return None
    try:
        filename = inspect.getsourcefile(obj)
    except TypeError:
        return None
    if (filename is None):
        return None
    (_, linenum) = inspect.getsourcelines(obj)
    assert isinstance(linenum, six.integer_types)
    filename = os.path.realpath(filename)
    relpath = _get_source_relative_path(filename)
    return 'https://github.com/chainer/chainer/blob/{}/{}#L{}'.format(tag, relpath, linenum)