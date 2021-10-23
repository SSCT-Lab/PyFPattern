def main():
    vm = None
    module = AnsibleModule(argument_spec=dict(hostname=dict(type='str', default=os.environ.get('VMWARE_HOST')), username=dict(type='str', default=os.environ.get('VMWARE_USER')), password=dict(type='str', no_log=True, default=os.environ.get('VMWARE_PASSWORD')), state=dict(required=False, choices=['poweredon', 'poweredoff', 'present', 'absent', 'restarted', 'reconfigured'], default='present'), validate_certs=dict(required=False, type='bool', default=True), template_src=dict(required=False, type='str', aliases=['template']), annotation=dict(required=False, type='str', aliases=['notes']), name=dict(required=True, type='str'), name_match=dict(required=False, type='str', default='first'), snapshot_op=dict(required=False, type='dict', default={
        
    }), uuid=dict(required=False, type='str'), folder=dict(required=False, type='str', default='/vm', aliases=['folder']), disk=dict(required=False, type='list'), nic=dict(required=False, type='list'), hardware=dict(required=False, type='dict', default={
        
    }), force=dict(required=False, type='bool', default=False), datacenter=dict(required=False, type='str', default=None), esxi_hostname=dict(required=False, type='str', default=None), cluster=dict(required=False, type='str', default=None), wait_for_ip_address=dict(required=False, type='bool', default=True), customize=dict(required=False, type='bool', default=False), ips=dict(required=False, type='str', default=None), dns_servers=dict(required=False, type='list', default=None), domain=dict(required=False, type='str', default=None), networks=dict(required=False, type='dict', default={
        
    })), supports_check_mode=True, mutually_exclusive=[], required_together=[['state', 'force'], ['template']])
    pyv = PyVmomiHelper(module)
    vm = pyv.getvm(name=module.params['name'], folder=module.params['folder'], uuid=module.params['uuid'], name_match=module.params['name_match'])
    if vm:
        if (module.params['state'] == 'absent'):
            if module.params['force']:
                result = pyv.set_powerstate(vm, 'poweredoff', module.params['force'])
            result = pyv.remove_vm(vm)
        elif (module.params['state'] in ['poweredon', 'poweredoff', 'restarted']):
            result = pyv.set_powerstate(vm, module.params['state'], module.params['force'])
        elif module.params['snapshot_op']:
            result = pyv.snapshot_vm(vm, module.params['name'], module.params['snapshot_op'])
        else:
            try:
                module.exit_json(instance=pyv.gather_facts(vm))
            except Exception:
                e = get_exception()
                module.fail_json(msg=('Fact gather failed with exception %s' % e))
    else:
        create_states = ['poweredon', 'poweredoff', 'present', 'restarted']
        if (module.params['state'] in create_states):
            poweron = (module.params['state'] != 'poweredoff')
            result = pyv.deploy_template(poweron=poweron, wait_for_ip=module.params['wait_for_ip_address'])
            result['changed'] = True
        elif (module.params['state'] == 'absent'):
            result = {
                'changed': False,
                'failed': False,
            }
        else:
            result = {
                'changed': False,
                'failed': False,
            }
    if (not ('failed' in result)):
        result['failed'] = False
    if result['failed']:
        module.fail_json(**result)
    else:
        module.exit_json(**result)