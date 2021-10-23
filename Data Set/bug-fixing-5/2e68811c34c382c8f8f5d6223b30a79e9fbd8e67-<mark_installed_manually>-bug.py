def mark_installed_manually(m, packages):
    if (not packages):
        return
    apt_mark_cmd_path = m.get_bin_path('apt-mark')
    if (apt_mark_cmd_path is None):
        m.warn('Could not find apt-mark binary, not marking package(s) as manually installed.')
        return
    cmd = ('%s manual %s' % (apt_mark_cmd_path, ' '.join(packages)))
    (rc, out, err) = m.run_command(cmd)
    if (APT_MARK_INVALID_OP in err):
        cmd = ('%s unmarkauto %s' % (apt_mark_cmd_path, ' '.join(packages)))
        (rc, out, err) = m.run_command(cmd)
    if (rc != 0):
        m.fail_json(msg=("'%s' failed: %s" % (cmd, err)), stdout=out, stderr=err, rc=rc)