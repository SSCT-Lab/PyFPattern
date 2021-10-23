

def main():
    argument_spec = dict(action=dict(required=True, choices=['create', 'add', 'compare', 'delete', 'delete_all']), snapshot_name=dict(type='str'), description=dict(type='str'), snapshot1=dict(type='str'), snapshot2=dict(type='str'), compare_option=dict(choices=['summary', 'ipv4routes', 'ipv6routes']), comparison_results_file=dict(type='str'), section=dict(type='str'), show_command=dict(type='str'), row_id=dict(type='str'), element_key1=dict(type='str'), element_key2=dict(type='str'), save_snapshot_locally=dict(type='bool', default=False), path=dict(type='str', default='./'))
    argument_spec.update(nxos_argument_spec)
    required_if = [('action', 'compare', ['snapshot1', 'snapshot2', 'comparison_results_file']), ('action', 'create', ['snapshot_name', 'description']), ('action', 'add', ['section', 'show_command', 'row_id', 'element_key1']), ('action', 'delete', ['snapshot_name'])]
    module = AnsibleModule(argument_spec=argument_spec, required_if=required_if, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    action = module.params['action']
    comparison_results_file = module.params['comparison_results_file']
    if (not os.path.isdir(module.params['path'])):
        module.fail_json(msg='{0} is not a valid directory name.'.format(module.params['path']))
    existing_snapshots = invoke('get_existing', module)
    action_results = invoke(('action_%s' % action), module, existing_snapshots)
    result = {
        'changed': False,
        'commands': [],
    }
    if (not module.check_mode):
        if (action == 'compare'):
            result['commands'] = []
            if (module.params['path'] and comparison_results_file):
                snapshot1 = module.params['snapshot1']
                snapshot2 = module.params['snapshot2']
                compare_option = module.params['compare_option']
                command = 'show snapshot compare {0} {1} {2}'.format(snapshot1, snapshot2, compare_option)
                content = execute_show_command(command, module)[0]
                if content:
                    write_on_file(content, comparison_results_file, module)
        else:
            if action_results:
                load_config(module, action_results)
                result['commands'] = action_results
                result['changed'] = True
            if ((action == 'create') and module.params['path'] and module.params['save_snapshot_locally']):
                command = 'show snapshot dump {} | json'.format(module.params['snapshot_name'])
                content = execute_show_command(command, module)[0]
                if content:
                    write_on_file(str(content), module.params['snapshot_name'], module)
    module.exit_json(**result)
