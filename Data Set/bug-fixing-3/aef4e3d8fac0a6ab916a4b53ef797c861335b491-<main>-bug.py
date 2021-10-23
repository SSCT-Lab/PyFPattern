def main():
    argument_spec = dict(action=dict(required=True, choices=['create', 'add', 'compare', 'delete', 'delete_all']), snapshot_name=dict(type='str'), description=dict(type='str'), snapshot1=dict(type='str'), snapshot2=dict(type='str'), compare_option=dict(choices=['summary', 'ipv4routes', 'ipv6routes']), comparison_results_file=dict(type='str'), section=dict(type='str'), show_command=dict(type='str'), row_id=dict(type='str'), element_key1=dict(type='str'), element_key2=dict(type='str'), save_snapshot_locally=dict(type='bool', default=False), path=dict(type='str', default='./'))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    action = module.params['action']
    comparison_results_file = module.params['comparison_results_file']
    CREATE_PARAMS = ['snapshot_name', 'description']
    ADD_PARAMS = ['section', 'show_command', 'row_id', 'element_key1']
    COMPARE_PARAMS = ['snapshot1', 'snapshot2', 'comparison_results_file']
    if (not os.path.isdir(module.params['path'])):
        module.fail_json(msg='{0} is not a valid directory name.'.format(module.params['path']))
    if (action == 'create'):
        for param in CREATE_PARAMS:
            if (not module.params[param]):
                module.fail_json(msg='snapshot_name and description are required when action=create')
    elif (action == 'add'):
        for param in ADD_PARAMS:
            if (not module.params[param]):
                module.fail_json(msg='section, show_command, row_id and element_key1 are required when action=add')
    elif (action == 'compare'):
        for param in COMPARE_PARAMS:
            if (not module.params[param]):
                module.fail_json(msg='snapshot1 and snapshot2 are required when action=create')
    elif ((action == 'delete') and (not module.params['snapshot_name'])):
        module.fail_json(msg='snapshot_name is required when action=delete')
    existing_snapshots = invoke('get_existing', module)
    final_snapshots = existing_snapshots
    changed = False
    action_results = invoke(('action_%s' % action), module, existing_snapshots)
    result = {
        
    }
    written_file = ''
    if (module.check_mode and (action != 'compare')):
        module.exit_json(changed=True, commands=action_results)
    elif (action == 'compare'):
        written_file = write_on_file(action_results, module.params['comparison_results_file'], module)
        result['updates'] = []
    elif action_results:
        load_config(module, action_results)
        changed = True
        final_snapshots = invoke('get_existing', module)
        result['updates'] = action_results
        if ((action == 'create') and module.params['save_snapshot_locally']):
            snapshot = get_snapshot(module)
            written_file = write_on_file(snapshot, module.params['snapshot_name'], module)
    result['changed'] = changed
    if (module._verbosity > 0):
        end_state = invoke('get_existing', module)
        result['final_snapshots'] = final_snapshots
        result['existing_snapshots'] = existing_snapshots
        if written_file:
            result['report_file'] = written_file
    module.exit_json(**result)