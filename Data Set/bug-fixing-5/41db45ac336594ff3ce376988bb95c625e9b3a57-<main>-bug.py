def main():
    module = AnsibleModule(argument_spec=dict(dest=dict(type='path'), repo=dict(type='str', required=True, aliases=['name', 'repository']), revision=dict(type='str', default='HEAD', aliases=['rev', 'version']), force=dict(type='bool', default=False), username=dict(type='str'), password=dict(type='str', no_log=True), executable=dict(type='path'), export=dict(type='bool', default=False), checkout=dict(type='bool', default=True), update=dict(type='bool', default=True), switch=dict(type='bool', default=True), in_place=dict(type='bool', default=False)), supports_check_mode=True)
    dest = module.params['dest']
    repo = module.params['repo']
    revision = module.params['revision']
    force = module.params['force']
    username = module.params['username']
    password = module.params['password']
    svn_path = (module.params['executable'] or module.get_bin_path('svn', True))
    export = module.params['export']
    switch = module.params['switch']
    checkout = module.params['checkout']
    update = module.params['update']
    in_place = module.params['in_place']
    module.run_command_environ_update = dict(LANG='C', LC_MESSAGES='C')
    if ((not dest) and (checkout or update or export)):
        module.fail_json(msg='the destination directory must be specified unless checkout=no, update=no, and export=no')
    svn = Subversion(module, dest, repo, revision, username, password, svn_path)
    if ((not export) and (not update) and (not checkout)):
        module.exit_json(changed=False, after=svn.get_remote_revision())
    if (export or (not os.path.exists(dest))):
        before = None
        local_mods = False
        if module.check_mode:
            module.exit_json(changed=True)
        elif ((not export) and (not checkout)):
            module.exit_json(changed=False)
        if ((not export) and checkout):
            svn.checkout()
        else:
            svn.export(force=force)
    elif svn.is_svn_repo():
        if (not update):
            module.exit_json(changed=False)
        if module.check_mode:
            if (svn.has_local_mods() and (not force)):
                module.fail_json(msg='ERROR: modified files exist in the repository.')
            (check, before, after) = svn.needs_update()
            module.exit_json(changed=check, before=before, after=after)
        before = svn.get_revision()
        local_mods = svn.has_local_mods()
        if switch:
            svn.switch()
        if local_mods:
            if force:
                svn.revert()
            else:
                module.fail_json(msg='ERROR: modified files exist in the repository.')
        svn.update()
    elif in_place:
        before = None
        svn.checkout(force=True)
        local_mods = svn.has_local_mods()
        if (local_mods and force):
            svn.revert()
    else:
        module.fail_json(msg=('ERROR: %s folder already exists, but its not a subversion repository.' % (dest,)))
    if export:
        module.exit_json(changed=True)
    else:
        after = svn.get_revision()
        changed = ((before != after) or local_mods)
        module.exit_json(changed=changed, before=before, after=after)