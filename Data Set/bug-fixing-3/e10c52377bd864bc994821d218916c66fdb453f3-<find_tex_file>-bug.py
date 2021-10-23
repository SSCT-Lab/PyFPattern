def find_tex_file(filename, format=None):
    "\n    Find a file in the texmf tree.\n\n    Calls :program:`kpsewhich` which is an interface to the kpathsea\n    library [1]_. Most existing TeX distributions on Unix-like systems use\n    kpathsea. It is also available as part of MikTeX, a popular\n    distribution on Windows.\n\n    Parameters\n    ----------\n    filename : string or bytestring\n    format : string or bytestring\n        Used as the value of the `--format` option to :program:`kpsewhich`.\n        Could be e.g. 'tfm' or 'vf' to limit the search to that type of files.\n\n    References\n    ----------\n\n    .. [1] `Kpathsea documentation <http://www.tug.org/kpathsea/>`_\n        The library that :program:`kpsewhich` is part of.\n    "
    cmd = [str('kpsewhich')]
    if (format is not None):
        cmd += [('--format=' + format)]
    cmd += [filename]
    matplotlib.verbose.report(('find_tex_file(%s): %s' % (filename, cmd)), 'debug')
    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = pipe.communicate()[0].rstrip()
    matplotlib.verbose.report(('find_tex_file result: %s' % result), 'debug')
    return result.decode('ascii')