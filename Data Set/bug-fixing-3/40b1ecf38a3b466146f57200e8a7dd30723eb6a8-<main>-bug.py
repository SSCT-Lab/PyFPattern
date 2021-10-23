def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True), state=dict(default='present', choices=PACKAGE_STATE_MAP.keys()), url=dict(default=None), timeout=dict(default='1m'), force=dict(default=False), plugin_bin=dict(type='path'), plugin_dir=dict(default='/usr/share/elasticsearch/plugins/', type='path'), proxy_host=dict(default=None), proxy_port=dict(default=None), version=dict(default=None)), supports_check_mode=True)
    name = module.params['name']
    state = module.params['state']
    url = module.params['url']
    timeout = module.params['timeout']
    force = module.params['force']
    plugin_bin = module.params['plugin_bin']
    plugin_dir = module.params['plugin_dir']
    proxy_host = module.params['proxy_host']
    proxy_port = module.params['proxy_port']
    version = module.params['version']
    plugin_bin = get_plugin_bin(module, plugin_bin)
    present = is_plugin_present(parse_plugin_repo(name), plugin_dir)
    if ((present and (state == 'present')) or ((state == 'absent') and (not present))):
        module.exit_json(changed=False, name=name, state=state)
    if (state == 'present'):
        (changed, cmd, out, err) = install_plugin(module, plugin_bin, name, version, url, proxy_host, proxy_port, timeout, force)
    elif (state == 'absent'):
        (changed, cmd, out, err) = remove_plugin(module, plugin_bin, name)
    module.exit_json(changed=changed, cmd=cmd, name=name, state=state, url=url, timeout=timeout, stdout=out, stderr=err)