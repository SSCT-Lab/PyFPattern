def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(state=dict(type='str', default='present', choices=['absent', 'poweredoff', 'poweredon', 'present', 'rebootguest', 'restarted', 'shutdownguest', 'suspended']), template=dict(type='str', aliases=['template_src']), is_template=dict(type='bool', default=False), annotation=dict(type='str', aliases=['notes']), customvalues=dict(type='list', default=[]), name=dict(type='str'), name_match=dict(type='str', choices=['first', 'last'], default='first'), uuid=dict(type='str'), folder=dict(type='str'), guest_id=dict(type='str'), disk=dict(type='list', default=[]), cdrom=dict(type='dict', default={
        
    }), hardware=dict(type='dict', default={
        
    }), force=dict(type='bool', default=False), datacenter=dict(type='str', default='ha-datacenter'), esxi_hostname=dict(type='str'), cluster=dict(type='str'), wait_for_ip_address=dict(type='bool', default=False), state_change_timeout=dict(type='int', default=0), snapshot_src=dict(type='str'), linked_clone=dict(type='bool', default=False), networks=dict(type='list', default=[]), resource_pool=dict(type='str'), customization=dict(type='dict', default={
        
    }, no_log=True), customization_spec=dict(type='str', default=None), vapp_properties=dict(type='list', default=[]), datastore=dict(type='str'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, mutually_exclusive=[['cluster', 'esxi_hostname']], required_one_of=[['name', 'uuid']])
    result = {
        'failed': False,
        'changed': False,
    }
    pyv = PyVmomiHelper(module)
    vm = pyv.get_vm()
    if vm:
        if (module.params['state'] == 'absent'):
            if module.check_mode:
                result.update(vm_name=vm.name, changed=True, current_powerstate=vm.summary.runtime.powerState.lower(), desired_operation='remove_vm')
                module.exit_json(**result)
            if module.params['force']:
                set_vm_power_state(pyv.content, vm, 'poweredoff', module.params['force'])
            result = pyv.remove_vm(vm)
        elif (module.params['state'] == 'present'):
            if module.check_mode:
                result.update(vm_name=vm.name, changed=True, desired_operation='reconfigure_vm')
                module.exit_json(**result)
            result = pyv.reconfigure_vm()
        elif (module.params['state'] in ['poweredon', 'poweredoff', 'restarted', 'suspended', 'shutdownguest', 'rebootguest']):
            if module.check_mode:
                result.update(vm_name=vm.name, changed=True, current_powerstate=vm.summary.runtime.powerState.lower(), desired_operation='set_vm_power_state')
                module.exit_json(**result)
            tmp_result = set_vm_power_state(pyv.content, vm, module.params['state'], module.params['force'], module.params['state_change_timeout'])
            if tmp_result['changed']:
                result['changed'] = True
            if (not tmp_result['failed']):
                result['failed'] = False
            result['instance'] = tmp_result['instance']
        else:
            raise AssertionError()
    elif (module.params['state'] in ['poweredon', 'poweredoff', 'present', 'restarted', 'suspended']):
        if module.check_mode:
            result.update(changed=True, desired_operation='deploy_vm')
            module.exit_json(**result)
        result = pyv.deploy_vm()
        if result['failed']:
            module.fail_json(msg=('Failed to create a virtual machine : %s' % result['msg']))
    if result['failed']:
        module.fail_json(**result)
    else:
        module.exit_json(**result)