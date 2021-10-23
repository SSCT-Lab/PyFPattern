def run(self, tmp=None, task_vars=None):
    ' handler for fetch operations '
    if (task_vars is None):
        task_vars = dict()
    result = super(ActionModule, self).run(tmp, task_vars)
    if self._play_context.check_mode:
        result['skipped'] = True
        result['msg'] = 'check mode not (yet) supported for this module'
        return result
    source = self._task.args.get('src', None)
    dest = self._task.args.get('dest', None)
    flat = boolean(self._task.args.get('flat'))
    fail_on_missing = boolean(self._task.args.get('fail_on_missing'))
    validate_checksum = boolean(self._task.args.get('validate_checksum', self._task.args.get('validate_md5', True)))
    if (('validate_md5' in self._task.args) and ('validate_checksum' in self._task.args)):
        result['failed'] = True
        result['msg'] = 'validate_checksum and validate_md5 cannot both be specified'
        return result
    if ('validate_md5' in self._task.args):
        display.deprecated('Use validate_checksum instead of validate_md5', version='2.8')
    if ((source is None) or (dest is None)):
        result['failed'] = True
        result['msg'] = 'src and dest are required'
        return result
    source = self._connection._shell.join_path(source)
    source = self._remote_expand_user(source)
    remote_checksum = None
    if (not self._play_context.become):
        remote_checksum = self._remote_checksum(source, all_vars=task_vars, follow=True)
    remote_data = None
    if (remote_checksum in ('1', '2', None)):
        slurpres = self._execute_module(module_name='slurp', module_args=dict(src=source), task_vars=task_vars, tmp=tmp)
        if slurpres.get('failed'):
            if ((not fail_on_missing) and (slurpres.get('msg').startswith('file not found') or (remote_checksum == '1'))):
                result['msg'] = 'the remote file does not exist, not transferring, ignored'
                result['file'] = source
                result['changed'] = False
            else:
                result.update(slurpres)
            return result
        else:
            if (slurpres['encoding'] == 'base64'):
                remote_data = base64.b64decode(slurpres['content'])
            if (remote_data is not None):
                remote_checksum = checksum_s(remote_data)
            remote_source = slurpres.get('source')
            if (remote_source and (remote_source != source)):
                source = remote_source
    if (os.path.sep not in self._connection._shell.join_path('a', '')):
        source = self._connection._shell._unquote(source)
        source_local = source.replace('\\', '/')
    else:
        source_local = source
    dest = os.path.expanduser(dest)
    if flat:
        if dest.endswith(os.sep):
            base = os.path.basename(source_local)
            dest = os.path.join(dest, base)
        if (not dest.startswith('/')):
            dest = self._loader.path_dwim(dest)
    else:
        if ('inventory_hostname' in task_vars):
            target_name = task_vars['inventory_hostname']
        else:
            target_name = self._play_context.remote_addr
        dest = ('%s/%s/%s' % (self._loader.path_dwim(dest), target_name, source_local))
    dest = dest.replace('//', '/')
    if (remote_checksum in ('0', '1', '2', '3', '4', '5')):
        result['changed'] = False
        result['file'] = source
        if (remote_checksum == '0'):
            result['msg'] = 'unable to calculate the checksum of the remote file'
        elif (remote_checksum == '1'):
            result['msg'] = 'the remote file does not exist'
        elif (remote_checksum == '2'):
            result['msg'] = 'no read permission on remote file'
        elif (remote_checksum == '3'):
            result['msg'] = 'remote file is a directory, fetch cannot work on directories'
        elif (remote_checksum == '4'):
            result['msg'] = "python isn't present on the system.  Unable to compute checksum"
        elif (remote_checksum == '5'):
            result['msg'] = 'stdlib json or simplejson was not found on the remote machine. Only the raw module can work without those installed'
        if fail_on_missing:
            result['failed'] = True
            del result['changed']
        else:
            result['msg'] += ', not transferring, ignored'
        return result
    local_checksum = checksum(dest)
    if (remote_checksum != local_checksum):
        makedirs_safe(os.path.dirname(dest))
        if (remote_data is None):
            self._connection.fetch_file(source, dest)
        else:
            try:
                f = open(to_bytes(dest, errors='surrogate_or_strict'), 'wb')
                f.write(remote_data)
                f.close()
            except (IOError, OSError) as e:
                raise AnsibleError(('Failed to fetch the file: %s' % e))
        new_checksum = secure_hash(dest)
        try:
            new_md5 = md5(dest)
        except ValueError:
            new_md5 = None
        if (validate_checksum and (new_checksum != remote_checksum)):
            result.update(dict(failed=True, md5sum=new_md5, msg='checksum mismatch', file=source, dest=dest, remote_md5sum=None, checksum=new_checksum, remote_checksum=remote_checksum))
        else:
            result.update({
                'changed': True,
                'md5sum': new_md5,
                'dest': dest,
                'remote_md5sum': None,
                'checksum': new_checksum,
                'remote_checksum': remote_checksum,
            })
    else:
        try:
            local_md5 = md5(dest)
        except ValueError:
            local_md5 = None
        result.update(dict(changed=False, md5sum=local_md5, file=source, dest=dest, checksum=local_checksum))
    return result