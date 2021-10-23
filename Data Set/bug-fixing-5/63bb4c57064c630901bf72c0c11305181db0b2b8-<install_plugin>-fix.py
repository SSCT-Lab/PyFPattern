def install_plugin(module, plugin_bin, plugin_name, url, timeout, kibana_version='4.6'):
    if (LooseVersion(kibana_version) > LooseVersion('4.6')):
        kibana_plugin_bin = os.path.join(os.path.dirname(plugin_bin), 'kibana-plugin')
        cmd_args = [kibana_plugin_bin, 'install']
        if url:
            cmd_args.append(url)
        else:
            cmd_args.append(plugin_name)
    else:
        cmd_args = [plugin_bin, 'plugin', PACKAGE_STATE_MAP['present'], plugin_name]
        if url:
            cmd_args.append(('--url %s' % url))
    if timeout:
        cmd_args.append(('--timeout %s' % timeout))
    cmd = ' '.join(cmd_args)
    if module.check_mode:
        return (True, cmd, 'check mode', '')
    (rc, out, err) = module.run_command(cmd)
    if (rc != 0):
        reason = parse_error(out)
        module.fail_json(msg=reason)
    return (True, cmd, out, err)