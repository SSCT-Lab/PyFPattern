

def main():
    module = AnsibleModule(argument_spec=dict(src=dict(type='str', required=True), dest=dict(type='str', required=True), dest_port=dict(type='int'), delete=dict(type='bool', default=False), private_key=dict(type='path'), rsync_path=dict(type='str'), _local_rsync_path=dict(type='path', default='rsync'), _substitute_controller=dict(type='bool', default=False), archive=dict(type='bool', default=True), checksum=dict(type='bool', default=False), compress=dict(type='bool', default=True), existing_only=dict(type='bool', default=False), dirs=dict(type='bool', default=False), recursive=dict(type='bool'), links=dict(type='bool'), copy_links=dict(type='bool', default=False), perms=dict(type='bool'), times=dict(type='bool'), owner=dict(type='bool'), group=dict(type='bool'), set_remote_user=dict(type='bool', default=True), rsync_timeout=dict(type='int', default=0), rsync_opts=dict(type='list'), ssh_args=dict(type='str'), partial=dict(type='bool', default=False), verify_host=dict(type='bool', default=False), mode=dict(type='str', default='push', choices=['pull', 'push']), link_dest=dict(type='list')), supports_check_mode=True)
    if module.params['_substitute_controller']:
        try:
            source = substitute_controller(module.params['src'])
            dest = substitute_controller(module.params['dest'])
        except ValueError:
            module.fail_json(msg='Could not determine controller hostname for rsync to send to')
    else:
        source = module.params['src']
        dest = module.params['dest']
    dest_port = module.params['dest_port']
    delete = module.params['delete']
    private_key = module.params['private_key']
    rsync_path = module.params['rsync_path']
    rsync = module.params.get('_local_rsync_path', 'rsync')
    rsync_timeout = module.params.get('rsync_timeout', 'rsync_timeout')
    archive = module.params['archive']
    checksum = module.params['checksum']
    compress = module.params['compress']
    existing_only = module.params['existing_only']
    dirs = module.params['dirs']
    partial = module.params['partial']
    recursive = module.params['recursive']
    links = module.params['links']
    copy_links = module.params['copy_links']
    perms = module.params['perms']
    times = module.params['times']
    owner = module.params['owner']
    group = module.params['group']
    rsync_opts = module.params['rsync_opts']
    ssh_args = module.params['ssh_args']
    verify_host = module.params['verify_host']
    link_dest = module.params['link_dest']
    if ('/' not in rsync):
        rsync = module.get_bin_path(rsync, required=True)
    cmd = [rsync, '--delay-updates', '-F']
    if compress:
        cmd.append('--compress')
    if rsync_timeout:
        cmd.append(('--timeout=%s' % rsync_timeout))
    if module.check_mode:
        cmd.append('--dry-run')
    if delete:
        cmd.append('--delete-after')
    if existing_only:
        cmd.append('--existing')
    if checksum:
        cmd.append('--checksum')
    if copy_links:
        cmd.append('--copy-links')
    if archive:
        cmd.append('--archive')
        if (recursive is False):
            cmd.append('--no-recursive')
        if (links is False):
            cmd.append('--no-links')
        if (perms is False):
            cmd.append('--no-perms')
        if (times is False):
            cmd.append('--no-times')
        if (owner is False):
            cmd.append('--no-owner')
        if (group is False):
            cmd.append('--no-group')
    else:
        if (recursive is True):
            cmd.append('--recursive')
        if (links is True):
            cmd.append('--links')
        if (perms is True):
            cmd.append('--perms')
        if (times is True):
            cmd.append('--times')
        if (owner is True):
            cmd.append('--owner')
        if (group is True):
            cmd.append('--group')
    if dirs:
        cmd.append('--dirs')
    if (source.startswith('rsync://') and dest.startswith('rsync://')):
        module.fail_json(msg='either src or dest must be a localhost', rc=1)
    if is_rsh_needed(source, dest):
        ssh_cmd = [module.get_bin_path('ssh', required=True), '-S', 'none']
        if (private_key is not None):
            ssh_cmd.extend(['-i', private_key])
        if (dest_port is not None):
            ssh_cmd.extend(['-o', ('Port=%s' % dest_port)])
        if (not verify_host):
            ssh_cmd.extend(['-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null'])
        ssh_cmd_str = ' '.join((shlex_quote(arg) for arg in ssh_cmd))
        if ssh_args:
            ssh_cmd_str += (' %s' % ssh_args)
        cmd.append(('--rsh=%s' % ssh_cmd_str))
    if rsync_path:
        cmd.append(('--rsync-path=%s' % rsync_path))
    if rsync_opts:
        cmd.extend(rsync_opts)
    if partial:
        cmd.append('--partial')
    if link_dest:
        cmd.append('-H')
        cmd.append('-vv')
        for x in link_dest:
            link_path = os.path.abspath(os.path.expanduser(x))
            destination_path = os.path.abspath(os.path.dirname(dest))
            if (destination_path.find(link_path) == 0):
                module.fail_json(msg=('Hardlinking into a subdirectory of the source would cause recursion. %s and %s' % (destination_path, dest)))
            cmd.append(('--link-dest=%s' % link_path))
    changed_marker = '<<CHANGED>>'
    cmd.append((('--out-format=' + changed_marker) + '%i %n%L'))
    if ('@' not in source):
        source = os.path.expanduser(source)
    if ('@' not in dest):
        dest = os.path.expanduser(dest)
    cmd.append(source)
    cmd.append(dest)
    cmdstr = ' '.join(cmd)
    (rc, out, err) = module.run_command(cmd)
    if rc:
        return module.fail_json(msg=err, rc=rc, cmd=cmdstr)
    if link_dest:
        changed = ((changed_marker + '.') not in out)
    else:
        changed = (changed_marker in out)
    out_clean = out.replace(changed_marker, '')
    out_lines = out_clean.split('\n')
    while ('' in out_lines):
        out_lines.remove('')
    if module._diff:
        diff = {
            'prepared': out_clean,
        }
        return module.exit_json(changed=changed, msg=out_clean, rc=rc, cmd=cmdstr, stdout_lines=out_lines, diff=diff)
    return module.exit_json(changed=changed, msg=out_clean, rc=rc, cmd=cmdstr, stdout_lines=out_lines)
