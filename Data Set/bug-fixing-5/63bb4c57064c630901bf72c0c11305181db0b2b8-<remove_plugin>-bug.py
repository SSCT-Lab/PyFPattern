def remove_plugin(module, plugin_bin, plugin_name):
    cmd_args = [plugin_bin, 'plugin', PACKAGE_STATE_MAP['absent'], plugin_name]
    cmd = ' '.join(cmd_args)
    if module.check_mode:
        return (True, cmd, 'check mode', '')
    (rc, out, err) = module.run_command(cmd)
    if (rc != 0):
        reason = parse_error(out)
        module.fail_json(msg=reason)
    return (True, cmd, out, err)