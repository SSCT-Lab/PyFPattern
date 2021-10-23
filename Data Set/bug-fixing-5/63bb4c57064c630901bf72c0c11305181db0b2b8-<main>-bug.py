def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True), state=dict(default='present', choices=PACKAGE_STATE_MAP.keys()), url=dict(default=None), timeout=dict(default='1m'), plugin_bin=dict(default='/opt/kibana/bin/kibana', type='path'), plugin_dir=dict(default='/opt/kibana/installedPlugins/', type='path'), version=dict(default=None), force=dict(default='no', type='bool')), supports_check_mode=True)
    name = module.params['name']
    state = module.params['state']
    url = module.params['url']
    timeout = module.params['timeout']
    plugin_bin = module.params['plugin_bin']
    plugin_dir = module.params['plugin_dir']
    version = module.params['version']
    force = module.params['force']
    present = is_plugin_present(parse_plugin_repo(name), plugin_dir)
    if ((present and (state == 'present') and (not force)) or ((state == 'absent') and (not present) and (not force))):
        module.exit_json(changed=False, name=name, state=state)
    if version:
        name = ((name + '/') + version)
    if (state == 'present'):
        if force:
            remove_plugin(module, plugin_bin, name)
        (changed, cmd, out, err) = install_plugin(module, plugin_bin, name, url, timeout)
    elif (state == 'absent'):
        (changed, cmd, out, err) = remove_plugin(module, plugin_bin, name)
    module.exit_json(changed=changed, cmd=cmd, name=name, state=state, url=url, timeout=timeout, stdout=out, stderr=err)