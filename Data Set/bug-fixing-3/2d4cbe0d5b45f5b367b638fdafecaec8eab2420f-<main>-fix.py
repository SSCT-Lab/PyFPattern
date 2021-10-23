def main():
    module = AnsibleModule(argument_spec=dict(package=dict(default=None, aliases=['name'], type='list'), state=dict(default=portage_present_states[0], choices=(portage_present_states + portage_absent_states)), update=dict(default=False, type='bool'), deep=dict(default=False, type='bool'), newuse=dict(default=False, type='bool'), changed_use=dict(default=False, type='bool'), oneshot=dict(default=False, type='bool'), noreplace=dict(default=True, type='bool'), nodeps=dict(default=False, type='bool'), onlydeps=dict(default=False, type='bool'), depclean=dict(default=False, type='bool'), quiet=dict(default=False, type='bool'), verbose=dict(default=False, type='bool'), sync=dict(default=None, choices=['yes', 'web', 'no']), getbinpkg=dict(default=False, type='bool'), usepkgonly=dict(default=False, type='bool'), usepkg=dict(default=False, type='bool'), keepgoing=dict(default=False, type='bool'), jobs=dict(default=None, type='int'), loadavg=dict(default=None, type='float'), quietbuild=dict(default=False, type='bool'), quietfail=dict(default=False, type='bool')), required_one_of=[['package', 'sync', 'depclean']], mutually_exclusive=[['nodeps', 'onlydeps'], ['quiet', 'verbose'], ['quietbuild', 'verbose'], ['quietfail', 'verbose']], supports_check_mode=True)
    module.emerge_path = module.get_bin_path('emerge', required=True)
    module.equery_path = module.get_bin_path('equery', required=True)
    p = module.params
    if (p['sync'] and (p['sync'].strip() != 'no')):
        sync_repositories(module, webrsync=(p['sync'] == 'web'))
        if (not p['package']):
            module.exit_json(msg='Sync successfully finished.')
    packages = []
    if p['package']:
        packages.extend(p['package'])
    if p['depclean']:
        if (packages and (p['state'] not in portage_absent_states)):
            module.fail_json(msg=('Depclean can only be used with package when the state is one of: %s' % portage_absent_states))
        cleanup_packages(module, packages)
    elif (p['state'] in portage_present_states):
        emerge_packages(module, packages)
    elif (p['state'] in portage_absent_states):
        unmerge_packages(module, packages)