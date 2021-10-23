def remove_packages(module, packages, root):
    remove_c = 0
    for package in packages:
        if (not query_package(module, package, root)):
            continue
        cmd = ('%s --auto %s %s' % (URPME_PATH, root_option(root), package))
        (rc, stdout, stderr) = module.run_command(cmd, check_rc=False)
        if (rc != 0):
            module.fail_json(msg=('failed to remove %s' % package))
        remove_c += 1
    if (remove_c > 0):
        module.exit_json(changed=True, msg=('removed %s package(s)' % remove_c))
    module.exit_json(changed=False, msg='package(s) already absent')