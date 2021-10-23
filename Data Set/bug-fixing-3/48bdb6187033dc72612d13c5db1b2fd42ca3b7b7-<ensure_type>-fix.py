def ensure_type(value, value_type, origin=None):
    " return a configuration variable with casting\n    :arg value: The value to ensure correct typing of\n    :kwarg value_type: The type of the value.  This can be any of the following strings:\n        :boolean: sets the value to a True or False value\n        :bool: Same as 'boolean'\n        :integer: Sets the value to an integer or raises a ValueType error\n        :int: Same as 'integer'\n        :float: Sets the value to a float or raises a ValueType error\n        :list: Treats the value as a comma separated list.  Split the value\n            and return it as a python list.\n        :none: Sets the value to None\n        :path: Expands any environment variables and tilde's in the value.\n        :tmppath: Create a unique temporary directory inside of the directory\n            specified by value and return its path.\n        :temppath: Same as 'tmppath'\n        :tmp: Same as 'tmppath'\n        :pathlist: Treat the value as a typical PATH string.  (On POSIX, this\n            means colon separated strings.)  Split the value and then expand\n            each part for environment variables and tildes.\n        :pathspec: Treat the value as a PATH string. Expands any environment variables\n            tildes's in the value.\n        :str: Sets the value to string types.\n        :string: Same as 'str'\n    "
    basedir = None
    if (origin and os.path.isabs(origin) and os.path.exists(to_bytes(origin))):
        basedir = origin
    if value_type:
        value_type = value_type.lower()
    if (value_type in ('boolean', 'bool')):
        value = boolean(value, strict=False)
    elif (value is not None):
        if (value_type in ('integer', 'int')):
            value = int(value)
        elif (value_type == 'float'):
            value = float(value)
        elif (value_type == 'list'):
            if isinstance(value, string_types):
                value = [x.strip() for x in value.split(',')]
        elif (value_type == 'none'):
            if (value == 'None'):
                value = None
        elif (value_type == 'path'):
            value = resolve_path(value, basedir=basedir)
        elif (value_type in ('tmp', 'temppath', 'tmppath')):
            value = resolve_path(value, basedir=basedir)
            if (not os.path.exists(value)):
                makedirs_safe(value, 448)
            prefix = ('ansible-local-%s' % os.getpid())
            value = tempfile.mkdtemp(prefix=prefix, dir=value)
        elif (value_type == 'pathspec'):
            if isinstance(value, string_types):
                value = value.split(os.pathsep)
            value = [resolve_path(x, basedir=basedir) for x in value]
        elif (value_type == 'pathlist'):
            if isinstance(value, string_types):
                value = value.split(',')
            value = [resolve_path(x, basedir=basedir) for x in value]
        elif (value_type in ('str', 'string')):
            value = unquote(to_text(value, errors='surrogate_or_strict'))
        elif isinstance(value, string_types):
            value = unquote(value)
    return to_text(value, errors='surrogate_or_strict', nonstring='passthru')