

def main():
    module = AnsibleModule(argument_spec=dict(state=dict(default='present', choices=['present', 'installed', 'absent', 'removed', 'latest']), name=dict(type='list'), repository=dict(type='list'), update_cache=dict(default='no', type='bool'), upgrade=dict(default='no', type='bool'), available=dict(default='no', type='bool')), required_one_of=[['name', 'update_cache', 'upgrade']], mutually_exclusive=[['name', 'upgrade']], supports_check_mode=True)
    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')
    global APK_PATH
    APK_PATH = module.get_bin_path('apk', required=True)
    p = module.params
    if p['repository']:
        for r in p['repository']:
            APK_PATH = ('%s --repository %s --repositories-file /dev/null' % (APK_PATH, r))
    if (p['state'] in ['present', 'installed']):
        p['state'] = 'present'
    if (p['state'] in ['absent', 'removed']):
        p['state'] = 'absent'
    if p['update_cache']:
        update_package_db(module, ((not p['name']) and (not p['upgrade'])))
    if p['upgrade']:
        upgrade_packages(module, p['available'])
    if (p['state'] in ['present', 'latest']):
        install_packages(module, p['name'], p['state'])
    elif (p['state'] == 'absent'):
        remove_packages(module, p['name'])
