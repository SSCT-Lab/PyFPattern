def main():
    module = AnsibleModule(argument_spec=dict(name=dict(aliases=['pkg', 'package', 'cask'], required=False, type='list'), path=dict(default='/usr/local/bin', required=False, type='path'), state=dict(default='present', choices=['present', 'installed', 'absent', 'removed', 'uninstalled']), update_homebrew=dict(default=False, aliases=['update-brew'], type='bool'), install_options=dict(default=None, aliases=['options'], type='list')), supports_check_mode=True)
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
    if (state in ('absent', 'removed', 'uninstalled')):
        state = 'absent'
    update_homebrew = p['update_homebrew']
    p['install_options'] = (p['install_options'] or [])
    install_options = ['--{0}'.format(install_option) for install_option in p['install_options']]
    brew_cask = HomebrewCask(module=module, path=path, casks=casks, state=state, update_homebrew=update_homebrew, install_options=install_options)
    (failed, changed, message) = brew_cask.run()
    if failed:
        module.fail_json(msg=message)
    else:
        module.exit_json(changed=changed, msg=message)