def path_to_str(path):
    'Returns the file system path representation of a `PathLike` object, else as it is.\n\n  Args:\n    path: An object that can be converted to path representation.\n\n  Returns:\n    A `str` object.\n  '
    if hasattr(path, '__fspath__'):
        path = as_str_any(path.__fspath__())
    return path