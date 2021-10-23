def upgrade(module, pacman_path):
    cmdupgrade = ('%s --sync --sysupgrade --quiet --noconfirm %s' % (pacman_path, module.params['upgrade_extra_args']))
    cmdneedrefresh = ('%s --query --upgrades' % pacman_path)
    (rc, stdout, stderr) = module.run_command(cmdneedrefresh, check_rc=False)
    data = stdout.split('\n')
    data.remove('')
    packages = []
    diff = {
        'before': '',
        'after': '',
    }
    if (rc == 0):
        regex = re.compile('([\\w+\\-.@]+) (\\S+-\\S+) -> (\\S+-\\S+)')
        for p in data:
            m = regex.search(p)
            packages.append(m.group(1))
            if module._diff:
                diff['before'] += ('%s-%s\n' % (m.group(1), m.group(2)))
                diff['after'] += ('%s-%s\n' % (m.group(1), m.group(3)))
        if module.check_mode:
            module.exit_json(changed=True, msg=('%s package(s) would be upgraded' % len(data)), packages=packages, diff=diff)
        (rc, stdout, stderr) = module.run_command(cmdupgrade, check_rc=False)
        if (rc == 0):
            module.exit_json(changed=True, msg='System upgraded', packages=packages, diff=diff)
        else:
            module.fail_json(msg='Could not upgrade')
    else:
        module.exit_json(changed=False, msg='Nothing to upgrade', packages=packages)