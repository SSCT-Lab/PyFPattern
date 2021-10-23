def upgrade(m, mode='yes', force=False, default_release=None, use_apt_get=False, dpkg_options=expand_dpkg_options(DPKG_OPTIONS), autoremove=False):
    if autoremove:
        autoremove = '--auto-remove'
    else:
        autoremove = ''
    if m.check_mode:
        check_arg = '--simulate'
    else:
        check_arg = ''
    apt_cmd = None
    prompt_regex = None
    if ((mode == 'dist') or ((mode == 'full') and use_apt_get)):
        apt_cmd = APT_GET_CMD
        upgrade_command = ('dist-upgrade %s' % autoremove)
    elif ((mode == 'full') and (not use_apt_get)):
        apt_cmd = APTITUDE_CMD
        upgrade_command = 'full-upgrade'
    elif use_apt_get:
        apt_cmd = APT_GET_CMD
        upgrade_command = ('upgrade --with-new-pkgs %s' % autoremove)
    else:
        apt_cmd = APTITUDE_CMD
        upgrade_command = 'safe-upgrade'
        prompt_regex = '(^Do you want to ignore this warning and proceed anyway\\?|^\\*\\*\\*.*\\[default=.*\\])'
    if force:
        if (apt_cmd == APT_GET_CMD):
            force_yes = '--force-yes'
        else:
            force_yes = '--assume-yes --allow-untrusted'
    else:
        force_yes = ''
    if (apt_cmd is None):
        if use_apt_get:
            apt_cmd = APT_GET_CMD
        else:
            m.fail_json(msg="Unable to find APTITUDE in path. Please make sure to have APTITUDE in path or use 'force_apt_get=True'")
    apt_cmd_path = m.get_bin_path(apt_cmd, required=True)
    cmd = ('%s -y %s %s %s %s' % (apt_cmd_path, dpkg_options, force_yes, check_arg, upgrade_command))
    if default_release:
        cmd += (" -t '%s'" % (default_release,))
    (rc, out, err) = m.run_command(cmd, prompt_regex=prompt_regex)
    if m._diff:
        diff = parse_diff(out)
    else:
        diff = {
            
        }
    if rc:
        m.fail_json(msg=("'%s %s' failed: %s" % (apt_cmd, upgrade_command, err)), stdout=out, rc=rc)
    if (((apt_cmd == APT_GET_CMD) and (APT_GET_ZERO in out)) or ((apt_cmd == APTITUDE_CMD) and (APTITUDE_ZERO in out))):
        m.exit_json(changed=False, msg=out, stdout=out, stderr=err)
    m.exit_json(changed=True, msg=out, stdout=out, stderr=err, diff=diff)