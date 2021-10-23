def main():
    module = AnsibleModule(argument_spec=dict(state=dict(type='str', default='present', choices=['absent', 'build-dep', 'installed', 'latest', 'present', 'removed', 'present', 'fixed']), update_cache=dict(type='bool', aliases=['update-cache']), cache_valid_time=dict(type='int', default=0), purge=dict(type='bool', default=False), package=dict(type='list', aliases=['pkg', 'name']), deb=dict(type='path'), default_release=dict(type='str', aliases=['default-release']), install_recommends=dict(type='bool', aliases=['install-recommends']), force=dict(type='bool', default=False), upgrade=dict(type='str', choices=['dist', 'full', 'no', 'safe', 'yes']), dpkg_options=dict(type='str', default=DPKG_OPTIONS), autoremove=dict(type='bool', default=False), autoclean=dict(type='bool', default=False), policy_rc_d=dict(type='int', default=None), only_upgrade=dict(type='bool', default=False), force_apt_get=dict(type='bool', default=False), allow_unauthenticated=dict(type='bool', default=False, aliases=['allow-unauthenticated'])), mutually_exclusive=[['deb', 'package', 'upgrade']], required_one_of=[['autoremove', 'deb', 'package', 'update_cache', 'upgrade']], supports_check_mode=True)
    module.run_command_environ_update = APT_ENV_VARS
    if (not HAS_PYTHON_APT):
        if module.check_mode:
            module.fail_json(msg=('%s must be installed to use check mode. If run normally this module can auto-install it.' % PYTHON_APT))
        try:
            module.warn(('Updating cache and auto-installing missing dependency: %s' % PYTHON_APT))
            module.run_command(['apt-get', 'update'], check_rc=True)
            module.run_command(['apt-get', 'install', '--no-install-recommends', PYTHON_APT, '-y', '-q'], check_rc=True)
            global apt, apt_pkg
            import apt
            import apt.debfile
            import apt_pkg
        except ImportError:
            module.fail_json(msg=('Could not import python modules: apt, apt_pkg. Please install %s package.' % PYTHON_APT))
    global APTITUDE_CMD
    APTITUDE_CMD = module.get_bin_path('aptitude', False)
    global APT_GET_CMD
    APT_GET_CMD = module.get_bin_path('apt-get')
    p = module.params
    if (p['upgrade'] == 'no'):
        p['upgrade'] = None
    use_apt_get = p['force_apt_get']
    if ((not use_apt_get) and (not APTITUDE_CMD)):
        module.warn('Could not find aptitude. Using apt-get instead')
        use_apt_get = True
    updated_cache = False
    updated_cache_time = 0
    install_recommends = p['install_recommends']
    allow_unauthenticated = p['allow_unauthenticated']
    dpkg_options = expand_dpkg_options(p['dpkg_options'])
    autoremove = p['autoremove']
    autoclean = p['autoclean']
    if (p['state'] == 'installed'):
        module.deprecate("State 'installed' is deprecated. Using state 'present' instead.", version='2.9')
        p['state'] = 'present'
    if (p['state'] == 'removed'):
        module.deprecate("State 'removed' is deprecated. Using state 'absent' instead.", version='2.9')
        p['state'] = 'absent'
    cache = get_cache(module)
    try:
        if p['default_release']:
            try:
                apt_pkg.config['APT::Default-Release'] = p['default_release']
            except AttributeError:
                apt_pkg.Config['APT::Default-Release'] = p['default_release']
            cache.open(progress=None)
        (mtimestamp, updated_cache_time) = get_updated_cache_time()
        updated_cache = False
        if (p['update_cache'] or p['cache_valid_time']):
            now = datetime.datetime.now()
            tdelta = datetime.timedelta(seconds=p['cache_valid_time'])
            if (not ((mtimestamp + tdelta) >= now)):
                err = ''
                for retry in range(3):
                    try:
                        cache.update()
                        break
                    except apt.cache.FetchFailedException as e:
                        err = to_native(e)
                else:
                    module.fail_json(msg=('Failed to update apt cache: %s' % err))
                cache.open(progress=None)
                (mtimestamp, post_cache_update_time) = get_updated_cache_time()
                if (updated_cache_time != post_cache_update_time):
                    updated_cache = True
                updated_cache_time = post_cache_update_time
            if ((not p['package']) and (not p['upgrade']) and (not p['deb'])):
                module.exit_json(changed=updated_cache, cache_updated=updated_cache, cache_update_time=updated_cache_time)
        force_yes = p['force']
        if p['upgrade']:
            upgrade(module, p['upgrade'], force_yes, p['default_release'], use_apt_get, dpkg_options, autoremove, allow_unauthenticated)
        if p['deb']:
            if (p['state'] != 'present'):
                module.fail_json(msg='deb only supports state=present')
            if ('://' in p['deb']):
                p['deb'] = fetch_file(module, p['deb'])
            install_deb(module, p['deb'], cache, install_recommends=install_recommends, allow_unauthenticated=allow_unauthenticated, force=force_yes, dpkg_options=p['dpkg_options'])
        unfiltered_packages = (p['package'] or ())
        packages = [package for package in unfiltered_packages if (package != '*')]
        all_installed = ('*' in unfiltered_packages)
        latest = (p['state'] == 'latest')
        if (latest and all_installed):
            if packages:
                module.fail_json(msg='unable to install additional packages when upgrading all installed packages')
            upgrade(module, 'yes', force_yes, p['default_release'], use_apt_get, dpkg_options, autoremove, allow_unauthenticated)
        if packages:
            for package in packages:
                if (package.count('=') > 1):
                    module.fail_json(msg=('invalid package spec: %s' % package))
                if (latest and ('=' in package)):
                    module.fail_json(msg=('version number inconsistent with state=latest: %s' % package))
        if (not packages):
            if autoclean:
                cleanup(module, p['purge'], force=force_yes, operation='autoclean', dpkg_options=dpkg_options)
            if autoremove:
                cleanup(module, p['purge'], force=force_yes, operation='autoremove', dpkg_options=dpkg_options)
        if (p['state'] in ('latest', 'present', 'build-dep', 'fixed')):
            state_upgrade = False
            state_builddep = False
            state_fixed = False
            if (p['state'] == 'latest'):
                state_upgrade = True
            if (p['state'] == 'build-dep'):
                state_builddep = True
            if (p['state'] == 'fixed'):
                state_fixed = True
            (success, retvals) = install(module, packages, cache, upgrade=state_upgrade, default_release=p['default_release'], install_recommends=install_recommends, force=force_yes, dpkg_options=dpkg_options, build_dep=state_builddep, fixed=state_fixed, autoremove=autoremove, only_upgrade=p['only_upgrade'], allow_unauthenticated=allow_unauthenticated)
            retvals['cache_updated'] = updated_cache
            retvals['cache_update_time'] = updated_cache_time
            if success:
                module.exit_json(**retvals)
            else:
                module.fail_json(**retvals)
        elif (p['state'] == 'absent'):
            remove(module, packages, cache, p['purge'], force=force_yes, dpkg_options=dpkg_options, autoremove=autoremove)
    except apt.cache.LockFailedException:
        module.fail_json(msg='Failed to lock apt for exclusive operation')
    except apt.cache.FetchFailedException:
        module.fail_json(msg='Could not fetch updated apt files')