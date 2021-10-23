def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True, type='str', aliases=['service']), runlevel=dict(required=True, type='str'), action=dict(choices=['respawn', 'wait', 'once', 'boot', 'bootwait', 'powerfail', 'powerwait', 'off', 'hold', 'ondemand', 'initdefault', 'sysinit'], type='str'), command=dict(required=True, type='str'), insertafter=dict(type='str'), state=dict(choices=['present', 'absent'], required=True, type='str')), supports_check_mode=True)
    result = {
        'name': module.params['name'],
        'changed': False,
        'msg': '',
    }
    mkitab = module.get_bin_path('mkitab')
    rmitab = module.get_bin_path('rmitab')
    chitab = module.get_bin_path('chitab')
    rc = 0
    current_entry = check_current_entry(module)
    if (module.params['state'] == 'present'):
        new_entry = ((((((module.params['name'] + ':') + module.params['runlevel']) + ':') + module.params['action']) + ':') + module.params['command'])
        if ((not current_entry['exist']) or ((module.params['runlevel'] != current_entry['runlevel']) or (module.params['action'] != current_entry['action']) or (module.params['command'] != current_entry['command']))):
            if current_entry['exist']:
                if (not module.check_mode):
                    (rc, out, err) = module.run_command([chitab, new_entry])
                if (rc != 0):
                    module.fail_json(msg='could not change inittab', rc=rc, err=err)
                result['msg'] = (('changed inittab entry' + ' ') + current_entry['name'])
                result['changed'] = True
            elif (not current_entry['exist']):
                if module.params['insertafter']:
                    if (not module.check_mode):
                        (rc, out, err) = module.run_command([mkitab, '-i', module.params['insertafter'], new_entry])
                elif (not module.check_mode):
                    (rc, out, err) = module.run_command([mkitab, new_entry])
                if (rc != 0):
                    module.fail_json('could not adjust inittab', rc=rc, err=err)
                result['msg'] = (('add inittab entry' + ' ') + module.params['name'])
                result['changed'] = True
    elif (module.params['state'] == 'absent'):
        if current_entry['exist']:
            if (not module.check_mode):
                (rc, out, err) = module.run_command([rmitab, module.params['name']])
                if (rc != 0):
                    module.fail_json(msg='could not remove entry grom inittab)', rc=rc, err=err)
            result['msg'] = (('removed inittab entry' + ' ') + current_entry['name'])
            result['changed'] = True
    module.exit_json(**result)