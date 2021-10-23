def install_plugin(module, plugin_bin, plugin_name, version, src, url, proxy_host, proxy_port, timeout, force):
    cmd_args = [plugin_bin, PACKAGE_STATE_MAP['present']]
    is_old_command = (os.path.basename(plugin_bin) == 'plugin')
    if is_old_command:
        if timeout:
            cmd_args.append(('--timeout %s' % timeout))
        if version:
            plugin_name = ((plugin_name + '/') + version)
            cmd_args[2] = plugin_name
    if (proxy_host and proxy_port):
        cmd_args.append(('-DproxyHost=%s -DproxyPort=%s' % (proxy_host, proxy_port)))
    if url:
        cmd_args.append(('--url %s' % url))
    if force:
        cmd_args.append('--batch')
    if src:
        cmd_args.append(src)
    else:
        cmd_args.append(plugin_name)
    cmd = ' '.join(cmd_args)
    if module.check_mode:
        (rc, out, err) = (0, 'check mode', '')
    else:
        (rc, out, err) = module.run_command(cmd)
    if (rc != 0):
        reason = parse_error(out)
        module.fail_json(msg=("Installing plugin '%s' failed: %s" % (plugin_name, reason)), err=err)
    return (True, cmd, out, err)