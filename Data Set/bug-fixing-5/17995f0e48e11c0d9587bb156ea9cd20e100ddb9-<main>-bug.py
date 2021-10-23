def main():
    module = AnsibleModule(argument_spec=dict(dest=dict(type='path'), repo=dict(required=True, aliases=['name']), version=dict(default='HEAD'), remote=dict(default='origin'), refspec=dict(default=None), reference=dict(default=None), force=dict(default='no', type='bool'), depth=dict(default=None, type='int'), clone=dict(default='yes', type='bool'), update=dict(default='yes', type='bool'), verify_commit=dict(default='no', type='bool'), accept_hostkey=dict(default='no', type='bool'), key_file=dict(default=None, type='path', required=False), ssh_opts=dict(default=None, required=False), executable=dict(default=None, type='path'), bare=dict(default='no', type='bool'), recursive=dict(default='yes', type='bool'), track_submodules=dict(default='no', type='bool'), umask=dict(default=None, type='raw'), archive=dict(type='path')), supports_check_mode=True)
    dest = module.params['dest']
    repo = module.params['repo']
    version = module.params['version']
    remote = module.params['remote']
    refspec = module.params['refspec']
    force = module.params['force']
    depth = module.params['depth']
    update = module.params['update']
    allow_clone = module.params['clone']
    bare = module.params['bare']
    verify_commit = module.params['verify_commit']
    reference = module.params['reference']
    git_path = (module.params['executable'] or module.get_bin_path('git', True))
    key_file = module.params['key_file']
    ssh_opts = module.params['ssh_opts']
    umask = module.params['umask']
    archive = module.params['archive']
    result = dict(changed=False, warnings=list())
    if module.params['accept_hostkey']:
        if (ssh_opts is not None):
            if ('-o StrictHostKeyChecking=no' not in ssh_opts):
                ssh_opts += ' -o StrictHostKeyChecking=no'
        else:
            ssh_opts = '-o StrictHostKeyChecking=no'
    if (umask is not None):
        if (not isinstance(umask, string_types)):
            module.fail_json(msg='umask must be defined as a quoted octal integer')
        try:
            umask = int(umask, 8)
        except:
            module.fail_json(msg='umask must be an octal integer', details=str(sys.exc_info()[1]))
        os.umask(umask)
    if repo.startswith('/'):
        repo = ('file://' + repo)
    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')
    gitconfig = None
    if ((not dest) and allow_clone):
        module.fail_json(msg='the destination directory must be specified unless clone=no')
    elif dest:
        dest = os.path.abspath(dest)
        if bare:
            gitconfig = os.path.join(dest, 'config')
        else:
            gitconfig = os.path.join(dest, '.git', 'config')
    ssh_wrapper = write_ssh_wrapper()
    set_git_ssh(ssh_wrapper, key_file, ssh_opts)
    module.add_cleanup_file(path=ssh_wrapper)
    git_version_used = git_version(git_path, module)
    if ((depth is not None) and (git_version_used < LooseVersion('1.9.1'))):
        result['warnings'].append('Your git version is too old to fully support the depth argument. Falling back to full checkouts.')
        depth = None
    recursive = module.params['recursive']
    track_submodules = module.params['track_submodules']
    result.update(before=None)
    local_mods = False
    need_fetch = True
    if ((dest and (not os.path.exists(gitconfig))) or ((not dest) and (not allow_clone))):
        if (module.check_mode or (not allow_clone)):
            remote_head = get_remote_head(git_path, module, dest, version, repo, bare)
            result.update(changed=True, after=remote_head)
            if module._diff:
                diff = get_diff(module, git_path, dest, repo, remote, depth, bare, result['before'], result['after'])
                if diff:
                    result['diff'] = diff
            module.exit_json(**result)
        clone(git_path, module, repo, dest, remote, depth, version, bare, reference, refspec, verify_commit)
        need_fetch = False
    elif (not update):
        result['before'] = get_version(module, git_path, dest)
        result.update(after=result['before'])
        module.exit_json(**result)
    else:
        local_mods = has_local_mods(module, git_path, dest, bare)
        result['before'] = get_version(module, git_path, dest)
        if local_mods:
            if (not force):
                module.fail_json(msg='Local modifications exist in repository (force=no).', **result)
            if (not module.check_mode):
                reset(git_path, module, dest)
                result.update(changed=True, msg='Local modifications exist.')
        if module.check_mode:
            remote_url = get_remote_url(git_path, module, dest, remote)
            remote_url_changed = (remote_url and (remote_url != repo) and (unfrackgitpath(remote_url) != unfrackgitpath(repo)))
        else:
            remote_url_changed = set_remote_url(git_path, module, repo, dest, remote)
        result.update(remote_url_changed=remote_url_changed)
        if module.check_mode:
            remote_head = get_remote_head(git_path, module, dest, version, remote, bare)
            result.update(changed=((result['before'] != remote_head) or remote_url_changed), after=remote_head)
            if module._diff:
                diff = get_diff(module, git_path, dest, repo, remote, depth, bare, result['before'], result['after'])
                if diff:
                    result['diff'] = diff
            module.exit_json(**result)
        else:
            fetch(git_path, module, repo, dest, version, remote, depth, bare, refspec, git_version_used)
        result['after'] = get_version(module, git_path, dest)
    if (not bare):
        switch_version(git_path, module, dest, remote, version, verify_commit, depth)
    submodules_updated = False
    if (recursive and (not bare)):
        submodules_updated = submodules_fetch(git_path, module, remote, track_submodules, dest)
        if submodules_updated:
            result.update(submodules_changed=submodules_updated)
            if module.check_mode:
                result.update(changed=True, after=remote_head)
                module.exit_json(**result)
            submodule_update(git_path, module, dest, track_submodules, force=force)
    result['after'] = get_version(module, git_path, dest)
    if ((result['before'] != result['after']) or local_mods or submodules_updated or remote_url_changed):
        result.update(changed=True)
        if module._diff:
            diff = get_diff(module, git_path, dest, repo, remote, depth, bare, result['before'], result['after'])
            if diff:
                result['diff'] = diff
    if archive:
        if module.check_mode:
            result.update(changed=True)
            module.exit_json(**result)
        create_archive(git_path, module, dest, archive, version, repo, result)
    if ssh_wrapper:
        try:
            os.remove(ssh_wrapper)
        except OSError:
            pass
    module.exit_json(**result)