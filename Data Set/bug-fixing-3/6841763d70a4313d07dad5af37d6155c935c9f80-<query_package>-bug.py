def query_package(module, name):
    cmd = ('rpm -q %s' % name)
    (rc, stdout, stderr) = module.run_command(cmd, check_rc=False)
    if (rc == 0):
        return True
    else:
        return False