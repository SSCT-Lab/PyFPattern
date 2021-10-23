def main():
    module = AnsibleModule(argument_spec=dict(name=dict(aliases=['pkg'], type='list'), exclude=dict(required=False, default=None), state=dict(default='installed', choices=['absent', 'present', 'installed', 'removed', 'latest']), enablerepo=dict(), disablerepo=dict(), list=dict(), conf_file=dict(default=None), disable_gpg_check=dict(required=False, default='no', type='bool'), skip_broken=dict(required=False, default='no', aliases=[], type='bool'), update_cache=dict(required=False, default='no', aliases=['expire-cache'], type='bool'), validate_certs=dict(required=False, default='yes', type='bool'), installroot=dict(required=False, default='/', type='str'), install_repoquery=dict(required=False, default='yes', type='bool'), allow_downgrade=dict(required=False, default='no', type='bool'), security=dict(default='no', type='bool')), required_one_of=[['name', 'list']], mutually_exclusive=[['name', 'list']], supports_check_mode=True)
    error_msgs = []
    if (not HAS_RPM_PYTHON):
        error_msgs.append('The Python 2 bindings for rpm are needed for this module. If you require Python 3 support use the `dnf` Ansible module instead.')
    if (not HAS_YUM_PYTHON):
        error_msgs.append('The Python 2 yum module is needed for this module. If you require Python 3 support use the `dnf` Ansible module instead.')
    if error_msgs:
        module.fail_json(msg='. '.join(error_msgs))
    params = module.params
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
        security = params['security']
        allow_downgrade = params['allow_downgrade']
        results = ensure(module, state, pkg, params['conf_file'], enablerepo, disablerepo, disable_gpg_check, exclude, repoquery, skip_broken, security, params['installroot'], allow_downgrade)
        if repoquery:
            results['msg'] = ('%s %s' % (results.get('msg', ''), 'Warning: Due to potential bad behaviour with rhnplugin and certificates, used slower repoquery calls instead of Yum API.'))
    module.exit_json(**results)