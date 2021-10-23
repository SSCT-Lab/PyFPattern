

def _set_fstab_args(fstab_file):
    result = []
    if (fstab_file and (fstab_file != '/etc/fstab')):
        if get_platform().lower().endswith('bsd'):
            result.append('-F')
        else:
            result.append('-T')
        result.append(fstab_file)
    return result
