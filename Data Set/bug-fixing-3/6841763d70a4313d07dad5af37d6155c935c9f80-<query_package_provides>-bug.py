def query_package_provides(module, name):
    cmd = ('rpm -q --provides %s' % name)
    (rc, stdout, stderr) = module.run_command(cmd, check_rc=False)
    return (rc == 0)