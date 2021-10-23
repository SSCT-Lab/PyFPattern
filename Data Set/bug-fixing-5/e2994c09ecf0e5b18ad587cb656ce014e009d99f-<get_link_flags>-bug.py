@tf_export('sysconfig.get_link_flags')
def get_link_flags():
    'Get the link flags for custom operators.\n\n  Returns:\n    The link flags.\n  '
    flags = []
    if (not _MONOLITHIC_BUILD):
        flags.append(('-L%s' % get_lib()))
        flags.append(('-l:libtensorflow_framework.so.%s' % _VERSION.split('.')[0]))
    return flags