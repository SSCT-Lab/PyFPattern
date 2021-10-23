def query_package(module, name, root):
    cmd = ('rpm -q %s %s' % (name, root_option(root)))
    (rc, stdout, stderr) = module.run_command(cmd, check_rc=False)
    if (rc == 0):
        return True
    else:
        return False