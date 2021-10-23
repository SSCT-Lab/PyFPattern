def check_path(path, dir=False):
    errors = []
    type_name = ('directory' if dir else 'file')
    (parent, file_name) = os.path.split(path)
    (name, ext) = os.path.splitext(file_name)
    if (name.upper() in ILLEGAL_NAMES):
        errors.append(('Illegal %s name %s: %s' % (type_name, name.upper(), path)))
    if (file_name[(- 1)] in ILLEGAL_END_CHARS):
        errors.append(("Illegal %s name end-char '%s': %s" % (type_name, file_name[(- 1)], path)))
    bfile = to_bytes(file_name, encoding='utf-8')
    for char in ILLEGAL_CHARS:
        if (char in bfile):
            bpath = to_bytes(path, encoding='utf-8')
            errors.append(('Illegal char %s in %s name: %s' % (char, type_name, bpath)))
    return errors