def query_package(module, pacman_path, name, state='present'):
    'Query the package status in both the local system and the repository. Returns a boolean to indicate if the package is installed, a second\n    boolean to indicate if the package is up-to-date and a third boolean to indicate whether online information were available\n    '
    if (state == 'present'):
        lcmd = ('%s --query --info %s' % (pacman_path, name))
        (lrc, lstdout, lstderr) = module.run_command(lcmd, check_rc=False)
        if (lrc != 0):
            return (False, False, False)
        else:
            installed_name = get_name(module, lstdout)
            if (installed_name != name):
                return (False, False, False)
        lversion = get_version(lstdout)
        rcmd = ('%s --sync --info %s' % (pacman_path, name))
        (rrc, rstdout, rstderr) = module.run_command(rcmd, check_rc=False)
        rversion = get_version(rstdout, True)
        if (rrc == 0):
            return (True, (lversion == rversion), False)
        return (True, True, True)