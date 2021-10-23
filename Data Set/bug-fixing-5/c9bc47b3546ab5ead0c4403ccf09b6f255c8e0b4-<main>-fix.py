def main():
    module = AnsibleModule(argument_spec=dict(name=dict(aliases=['pkg', 'package', 'cask'], required=False, type='list'), path=dict(default='/usr/local/bin', required=False, type='path'), state=dict(default='present', choices=['present', 'installed', 'latest', 'upgraded', 'absent', 'removed', 'uninstalled']), sudo_password=dict(type='str', required=False, no_log=True), update_homebrew=dict(default=False, aliases=['update-brew'], type='bool'), install_options=dict(default=None, aliases=['options'], type='list'), accept_external_apps=dict(default=False, type='bool'), upgrade_all=dict(default=False, aliases=['upgrade'], type='bool'), greedy=dict(default=False, type='bool')), supports_check_mode=True)
    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')
    p = module.params
    if p['name']:
        casks = p['name']
    else:
        casks = None
    path = p['path']
    if path:
        path = path.split(':')
    state = p['state']
    if (state in ('present', 'installed')):
        state = 'installed'
    if (state in ('latest', 'upgraded')):
        state = 'upgraded'
    if (state in ('absent', 'removed', 'uninstalled')):
        state = 'absent'
    sudo_password = p['sudo_password']
    update_homebrew = p['update_homebrew']
    upgrade_all = p['upgrade_all']
    greedy = p['greedy']
    p['install_options'] = (p['install_options'] or [])
    install_options = ['--{0}'.format(install_option) for install_option in p['install_options']]
    accept_external_apps = p['accept_external_apps']
    brew_cask = HomebrewCask(module=module, path=path, casks=casks, state=state, sudo_password=sudo_password, update_homebrew=update_homebrew, install_options=install_options, accept_external_apps=accept_external_apps, upgrade_all=upgrade_all, greedy=greedy)
    (failed, changed, message) = brew_cask.run()
    if failed:
        module.fail_json(msg=message)
    else:
        module.exit_json(changed=changed, msg=message)