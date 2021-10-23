def contentfilter(fsname, pattern):
    '\n    Filter files which contain the given expression\n    :arg fsname: Filename to scan for lines matching a pattern\n    :arg pattern: Pattern to look for inside of line\n    :rtype: bool\n    :returns: True if one of the lines in fsname matches the pattern. Otherwise False\n    '
    if (pattern is None):
        return True
    prog = re.compile(pattern)
    try:
        with open(fsname) as f:
            for line in f:
                if prog.match(line):
                    return True
    except Exception:
        pass
    return False