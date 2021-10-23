

def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True, type='str'), type=dict(required=True, choices=['account', 'auth', 'password', 'session']), control=dict(required=True, type='str'), module_path=dict(required=True, type='str'), new_type=dict(required=False, choices=['account', 'auth', 'password', 'session']), new_control=dict(required=False, type='str'), new_module_path=dict(required=False, type='str'), module_arguments=dict(required=False, type='list'), state=dict(required=False, default='updated', choices=['before', 'after', 'updated', 'args_absent', 'args_present', 'absent']), path=dict(required=False, default='/etc/pam.d', type='str'), backup=dict(default=False, type='bool')), supports_check_mode=True, required_if=[('state', 'args_present', ['module_arguments']), ('state', 'args_absent', ['module_arguments']), ('state', 'before', ['new_control']), ('state', 'before', ['new_type']), ('state', 'before', ['new_module_path']), ('state', 'after', ['new_control']), ('state', 'after', ['new_type']), ('state', 'after', ['new_module_path'])])
    content = str()
    fname = os.path.join(module.params['path'], module.params['name'])
    backupdest = ''
    try:
        with open(fname, 'r') as service_file_obj:
            content = service_file_obj.read()
    except IOError as e:
        module.fail_json(msg=('Unable to open/read PAM module                             file %s with error %s.' % (fname, str(e))))
    service = PamdService(content)
    action = module.params['state']
    if (action == 'updated'):
        changes = service.update_rule(module.params['type'], module.params['control'], module.params['module_path'], module.params['new_type'], module.params['new_control'], module.params['new_module_path'], module.params['module_arguments'])
    elif (action == 'before'):
        changes = service.insert_before(module.params['type'], module.params['control'], module.params['module_path'], module.params['new_type'], module.params['new_control'], module.params['new_module_path'], module.params['module_arguments'])
    elif (action == 'after'):
        changes = service.insert_after(module.params['type'], module.params['control'], module.params['module_path'], module.params['new_type'], module.params['new_control'], module.params['new_module_path'], module.params['module_arguments'])
    elif (action == 'args_absent'):
        changes = service.remove_module_arguments(module.params['type'], module.params['control'], module.params['module_path'], module.params['module_arguments'])
    elif (action == 'args_present'):
        changes = service.add_module_arguments(module.params['type'], module.params['control'], module.params['module_path'], module.params['module_arguments'])
    elif (action == 'absent'):
        changes = service.remove(module.params['type'], module.params['control'], module.params['module_path'])
    (valid, msg) = service.validate()
    if (not valid):
        module.fail_json(msg=msg)
    if ((not module.check_mode) and (changes > 0)):
        pamd_file = os.path.realpath(fname)
        if module.params['backup']:
            backupdest = module.backup_local(fname)
            print('BACKUP DEST', backupdest)
        try:
            temp_file = NamedTemporaryFile(mode='w', dir=module.tmpdir)
            with open(temp_file.name, 'w') as fd:
                fd.write(str(service))
        except IOError:
            module.fail_json(msg=('Unable to create temporary                                     file %s' % temp_file))
        module.atomic_move(temp_file.name, pamd_file)
    facts = {
        
    }
    facts['pamd'] = {
        'changed': (changes > 0),
        'change_count': changes,
        'action': action,
        'backupdest': backupdest,
    }
    module.exit_json(changed=(changes > 0), ansible_facts=facts)
