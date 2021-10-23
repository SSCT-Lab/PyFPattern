def expand_package_groups(module, pacman_path, pkgs):
    expanded = []
    for pkg in pkgs:
        if pkg:
            cmd = ('%s -Sgq %s' % (pacman_path, pkg))
            (rc, stdout, stderr) = module.run_command(cmd, check_rc=False)
            if (rc == 0):
                for name in stdout.split('\n'):
                    name = name.strip()
                    if name:
                        expanded.append(name)
            else:
                expanded.append(pkg)
    return expanded