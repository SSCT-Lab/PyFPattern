def _is_present(name, version, installed_pkgs, pkg_command):
    'Return whether or not package is installed.'
    for pkg in installed_pkgs:
        if ('list' in pkg_command):
            pkg = pkg.replace('(', '').replace(')', '')
            if (',' in pkg):
                (pkg_name, pkg_version, _) = pkg.replace(',', '').split(' ')
            else:
                (pkg_name, pkg_version) = pkg.split(' ')
        elif ('freeze' in pkg_command):
            if ('==' in pkg):
                (pkg_name, pkg_version) = pkg.split('==')
            else:
                continue
        else:
            continue
        if ((pkg_name == name) and ((version is None) or (version == pkg_version))):
            return True
    return False