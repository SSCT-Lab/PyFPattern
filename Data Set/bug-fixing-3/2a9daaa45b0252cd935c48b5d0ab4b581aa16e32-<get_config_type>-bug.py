def get_config_type(cfile):
    ftype = None
    if (cfile is not None):
        ext = os.path.splitext(cfile)[(- 1)]
        if (ext in ('.ini', '.cfg')):
            ftype = 'ini'
        elif (ext in ('.yaml', '.yml')):
            ftype = 'yaml'
        else:
            raise AnsibleOptionsError(('Unsupported configuration file extension for %s: %s' % (cfile, to_native(ext))))
    return ftype