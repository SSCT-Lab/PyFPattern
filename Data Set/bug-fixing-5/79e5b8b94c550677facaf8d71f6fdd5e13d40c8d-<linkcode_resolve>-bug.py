def linkcode_resolve(domain, info):
    if ((domain != 'py') or (not info['module'])):
        return None
    rtd_version = os.environ.get('READTHEDOCS_VERSION')
    if (rtd_version == 'latest'):
        tag = 'master'
    else:
        tag = 'v{}'.format(__version__)
    repo_root_dir = os.path.realpath('..')
    obj = _import_object_from_name(info['module'], info['fullname'])
    try:
        filename = inspect.getsourcefile(obj)
    except TypeError:
        return None
    if (filename is None):
        return None
    (_, linenum) = inspect.getsourcelines(obj)
    assert isinstance(linenum, six.integer_types)
    filename = os.path.realpath(filename)
    if (not filename.startswith(repo_root_dir)):
        return None
    relpath = os.path.relpath(filename, repo_root_dir)
    return 'https://github.com/chainer/chainer/blob/{}/{}#L{}'.format(tag, relpath, linenum)