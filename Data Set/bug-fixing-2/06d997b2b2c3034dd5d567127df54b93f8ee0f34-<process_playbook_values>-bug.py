

def process_playbook_values(self):
    ' Get playbook values and perform input validation '
    argument_spec = dict(vrf=dict(type='str', default='management'), connect_ssh_port=dict(type='int', default=22), file_system=dict(type='str', default='bootflash:'), file_pull=dict(type='bool', default=False), file_pull_timeout=dict(type='int', default=300), file_pull_compact=dict(type='bool', default=False), file_pull_kstack=dict(type='bool', default=False), local_file=dict(type='path'), local_file_directory=dict(type='path'), remote_file=dict(type='path'), remote_scp_server=dict(type='str'), remote_scp_server_user=dict(type='str'), remote_scp_server_password=dict(no_log=True))
    playvals = {
        
    }
    for key in argument_spec.keys():
        playvals[key] = self._task.args.get(key, argument_spec[key].get('default'))
        if (playvals[key] is None):
            continue
        option_type = argument_spec[key].get('type', 'str')
        try:
            if (option_type == 'str'):
                playvals[key] = validation.check_type_str(playvals[key])
            elif (option_type == 'int'):
                playvals[key] = validation.check_type_int(playvals[key])
            elif (option_type == 'bool'):
                playvals[key] = validation.check_type_bool(playvals[key])
            elif (option_type == 'path'):
                playvals[key] = validation.check_type_path(playvals[key])
            else:
                raise AnsibleError('Unrecognized type <{0}> for playbook parameter <{1}>'.format(type, key))
        except (TypeError, ValueError) as e:
            raise AnsibleError(('argument %s is of type %s and we were unable to convert to %s: %s' % (key, type(playvals[key]), option_type, to_native(e))))
    if playvals['file_pull']:
        if (playvals.get('remote_file') is None):
            raise AnsibleError('Playbook parameter <remote_file> required when <file_pull> is True')
        if (playvals.get('remote_scp_server') is None):
            raise AnsibleError('Playbook parameter <remote_scp_server> required when <file_pull> is True')
    if (playvals['remote_scp_server'] or playvals['remote_scp_server_user']):
        if (None in (playvals['remote_scp_server'], playvals['remote_scp_server_user'])):
            params = '<remote_scp_server>, <remote_scp_server_user>'
            raise AnsibleError('Playbook parameters {0} must be set together'.format(params))
    return playvals
