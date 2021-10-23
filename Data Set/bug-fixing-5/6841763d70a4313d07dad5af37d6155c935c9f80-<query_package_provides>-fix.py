def query_package_provides(module, name, root):
    cmd = ('rpm -q --provides %s %s' % (name, root_option(root)))
    (rc, stdout, stderr) = module.run_command(cmd, check_rc=False)
    return (rc == 0)