

def main():
    module = AnsibleModule(argument_spec=dict(name=dict(type='list', aliases=['pkg']), exclude=dict(type='str'), state=dict(type='str', default='installed', choices=['absent', 'installed', 'latest', 'present', 'removed']), enablerepo=dict(type='str'), disablerepo=dict(type='str'), list=dict(type='str'), conf_file=dict(type='str'), disable_gpg_check=dict(type='bool', default=False), skip_broken=dict(type='bool', default=False), update_cache=dict(type='bool', default=False, aliases=['expire-cache']), validate_certs=dict(type='bool', default=True), installroot=dict(type='str', default='/'), update_only=dict(required=False, default='no', type='bool'), install_repoquery=dict(type='bool', default=True), allow_downgrade=dict(type='bool', default=False), security=dict(type='bool', default=False), enable_plugin=dict(type='list', default=[]), disable_plugin=dict(type='list', default=[])), required_one_of=[['name', 'list']], mutually_exclusive=[['name', 'list']], supports_check_mode=True)
    error_msgs = []
    if (not HAS_RPM_PYTHON):
        error_msgs.append('The Python 2 bindings for rpm are needed for this module. If you require Python 3 support use the `dnf` Ansible module instead.')
    if (not HAS_YUM_PYTHON):
        error_msgs.append('The Python 2 yum module is needed for this module. If you require Python 3 support use the `dnf` Ansible module instead.')
    if error_msgs:
        module.fail_json(msg='. '.join(error_msgs))
    params = module.params
    enable_plugin = params.get('enable_plugin', '')
    if enable_plugin:
        enable_plugin = ','.join(enable_plugin)
    disable_plugin = params.get('disable_plugin', '')
    if disable_plugin:
        disable_plugin = ','.join(disable_plugin)
    if params['list']:
        repoquerybin = ensure_yum_utils(module)
        if (not repoquerybin):
            module.fail_json(msg='repoquery is required to use list= with this module. Please install the yum-utils package.')
        results = {
            'results': list_stuff(module, repoquerybin, params['conf_file'], params['list'], params['installroot'], params['disablerepo'], params['enablerepo']),
        }
    else:
        my = yum_base(params['conf_file'], params['installroot'])
        my.conf
        repoquery = None
        try:
            yum_plugins = my.plugins._plugins
        except AttributeError:
            pass
        else:
            if ('rhnplugin' in yum_plugins):
                repoquerybin = ensure_yum_utils(module)
                if repoquerybin:
                    repoquery = [repoquerybin, '--show-duplicates', '--plugins', '--quiet']
                    if (params['installroot'] != '/'):
                        repoquery.extend(['--installroot', params['installroot']])
        pkg = [p.strip() for p in params['name']]
        exclude = params['exclude']
        state = params['state']
        enablerepo = params.get('enablerepo', '')
        disablerepo = params.get('disablerepo', '')
        disable_gpg_check = params['disable_gpg_check']
        skip_broken = params['skip_broken']
        update_only = params['update_only']
        security = params['security']
        allow_downgrade = params['allow_downgrade']
        results = ensure(module, state, pkg, params['conf_file'], enablerepo, disablerepo, disable_gpg_check, exclude, repoquery, skip_broken, update_only, security, params['installroot'], allow_downgrade, disable_plugin=disable_plugin, enable_plugin=enable_plugin)
        if repoquery:
            results['msg'] = ('%s %s' % (results.get('msg', ''), 'Warning: Due to potential bad behaviour with rhnplugin and certificates, used slower repoquery calls instead of Yum API.'))
    module.exit_json(**results)
