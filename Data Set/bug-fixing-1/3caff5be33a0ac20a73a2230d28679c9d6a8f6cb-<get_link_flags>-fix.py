

@tf_export('sysconfig.get_link_flags')
def get_link_flags():
    'Get the link flags for custom operators.\n\n  Returns:\n    The link flags.\n  '
    is_mac = (_platform.system() == 'Darwin')
    ver = _VERSION.split('.')[0]
    flags = []
    if (not _MONOLITHIC_BUILD):
        flags.append(('-L%s' % get_lib()))
        if is_mac:
            flags.append(('-ltensorflow_framework.%s' % ver))
        else:
            flags.append(('-l:libtensorflow_framework.so.%s' % ver))
    return flags
