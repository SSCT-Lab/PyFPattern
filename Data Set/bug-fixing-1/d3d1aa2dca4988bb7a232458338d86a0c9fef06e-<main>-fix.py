

def main():
    module = AnsibleModule(argument_spec=dict(src=dict(required=True), dest=dict(required=True), dest_port=dict(default=None, type='int'), delete=dict(default='no', type='bool'), private_key=dict(default=None), rsync_path=dict(default=None), _local_rsync_path=dict(default='rsync', type='path'), _substitute_controller=dict(default='no', type='bool'), archive=dict(default='yes', type='bool'), checksum=dict(default='no', type='bool'), compress=dict(default='yes', type='bool'), existing_only=dict(default='no', type='bool'), dirs=dict(default='no', type='bool'), recursive=dict(type='bool'), links=dict(type='bool'), copy_links=dict(type='bool'), perms=dict(type='bool'), times=dict(type='bool'), owner=dict(type='bool'), group=dict(type='bool'), set_remote_user=dict(default='yes', type='bool'), rsync_timeout=dict(type='int', default=0), rsync_opts=dict(type='list'), ssh_args=dict(type='str'), partial=dict(default='no', type='bool'), verify_host=dict(default='no', type='bool'), mode=dict(default='push', choices=['push', 'pull'])), supports_check_mode=True)
    if module.params['_substitute_controller']:
        try:
            source = (('"' + substitute_controller(module.params['src'])) + '"')
            dest = (('"' + substitute_controller(module.params['dest'])) + '"')
        except ValueError:
            module.fail_json(msg='Could not determine controller hostname for rsync to send to')
    else:
        source = (('"' + module.params['src']) + '"')
        dest = (('"' + module.params['dest']) + '"')
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
    if ('/' not in rsync):
        rsync = module.get_bin_path(rsync, required=True)
    ssh = module.get_bin_path('ssh', required=True)
    cmd = ('%s --delay-updates -F' % rsync)
    if compress:
        cmd = (cmd + ' --compress')
    if rsync_timeout:
        cmd = (cmd + (' --timeout=%s' % rsync_timeout))
    if module.check_mode:
        cmd = (cmd + ' --dry-run')
    if delete:
        cmd = (cmd + ' --delete-after')
    if existing_only:
        cmd = (cmd + ' --existing')
    if checksum:
        cmd = (cmd + ' --checksum')
    if archive:
        cmd = (cmd + ' --archive')
        if (recursive is False):
            cmd = (cmd + ' --no-recursive')
        if (links is False):
            cmd = (cmd + ' --no-links')
        if (copy_links is True):
            cmd = (cmd + ' --copy-links')
        if (perms is False):
            cmd = (cmd + ' --no-perms')
        if (times is False):
            cmd = (cmd + ' --no-times')
        if (owner is False):
            cmd = (cmd + ' --no-owner')
        if (group is False):
            cmd = (cmd + ' --no-group')
    else:
        if (recursive is True):
            cmd = (cmd + ' --recursive')
        if (links is True):
            cmd = (cmd + ' --links')
        if (copy_links is True):
            cmd = (cmd + ' --copy-links')
        if (perms is True):
            cmd = (cmd + ' --perms')
        if (times is True):
            cmd = (cmd + ' --times')
        if (owner is True):
            cmd = (cmd + ' --owner')
        if (group is True):
            cmd = (cmd + ' --group')
    if dirs:
        cmd = (cmd + ' --dirs')
    if (private_key is None):
        private_key = ''
    else:
        private_key = ('-i "%s"' % private_key)
    ssh_opts = '-S none'
    if (not verify_host):
        ssh_opts = ('%s -o StrictHostKeyChecking=no' % ssh_opts)
    if ssh_args:
        ssh_opts = ('%s %s' % (ssh_opts, ssh_args))
    if (source.startswith('"rsync://') and dest.startswith('"rsync://')):
        module.fail_json(msg='either src or dest must be a localhost', rc=1)
    if ((not source.startswith('"rsync://')) and (not dest.startswith('"rsync://'))):
        if (dest_port is not None):
            cmd += (" --rsh 'ssh %s %s -o Port=%s'" % (private_key, ssh_opts, dest_port))
        else:
            cmd += (" --rsh 'ssh %s %s'" % (private_key, ssh_opts))
    if rsync_path:
        cmd = (cmd + (' --rsync-path=%s' % rsync_path))
    if rsync_opts:
        cmd = ((cmd + ' ') + ' '.join(rsync_opts))
    if partial:
        cmd = (cmd + ' --partial')
    changed_marker = '<<CHANGED>>'
    cmd = (((cmd + " --out-format='") + changed_marker) + "%i %n%L'")
    if ('@' not in source):
        source = os.path.expanduser(source)
    if ('@' not in dest):
        dest = os.path.expanduser(dest)
    cmd = ' '.join([cmd, source, dest])
    cmdstr = cmd
    (rc, out, err) = module.run_command(cmd)
    if rc:
        return module.fail_json(msg=err, rc=rc, cmd=cmdstr)
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
        else:
            return module.exit_json(changed=changed, msg=out_clean, rc=rc, cmd=cmdstr, stdout_lines=out_lines)
