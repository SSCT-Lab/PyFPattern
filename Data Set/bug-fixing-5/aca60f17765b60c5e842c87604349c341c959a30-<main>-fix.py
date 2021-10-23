def main():
    module = AnsibleModule(argument_spec=dict(hostname=dict(type='str', default=os.environ.get('VMWARE_HOST')), username=dict(type='str', default=os.environ.get('VMWARE_USER')), password=dict(type='str', no_log=True, default=os.environ.get('VMWARE_PASSWORD')), state=dict(required=False, choices=['poweredon', 'poweredoff', 'present', 'absent', 'restarted', 'suspended', 'gatherfacts'], default='present'), validate_certs=dict(required=False, type='bool', default=True), template_src=dict(required=False, type='str', aliases=['template'], default=None), is_template=dict(required=False, type='bool', default=False), annotation=dict(required=False, type='str', aliases=['notes']), name=dict(required=True, type='str'), new_name=dict(required=False, type='str'), name_match=dict(required=False, type='str', default='first'), snapshot_op=dict(required=False, type='dict', default={
        
    }), uuid=dict(required=False, type='str'), folder=dict(required=False, type='str', default='/vm'), guest_id=dict(required=False, type='str', default=None), disk=dict(required=False, type='list', default=[]), hardware=dict(required=False, type='dict', default={
        
    }), force=dict(required=False, type='bool', default=False), datacenter=dict(required=False, type='str', default=None), esxi_hostname=dict(required=False, type='str', default=None), cluster=dict(required=False, type='str', default=None), wait_for_ip_address=dict(required=False, type='bool', default=True), networks=dict(required=False, type='dict', default={
        
    }), resource_pool=dict(required=False, type='str', default=None), customization=dict(required=False, type='dict', no_log=True, default={
        
    })), supports_check_mode=True, mutually_exclusive=[['esxi_hostname', 'cluster']], required_together=[['state', 'force'], ['template']])
    result = {
        'failed': False,
        'changed': False,
    }
    if ((not module.params['folder'].startswith('/vm')) and module.params['folder'].startswith('/')):
        module.params['folder'] = ('/vm%(folder)s' % module.params)
    module.params['folder'] = module.params['folder'].rstrip('/')
    pyv = PyVmomiHelper(module)
    vm = pyv.getvm(name=module.params['name'], folder=module.params['folder'], uuid=module.params['uuid'], name_match=module.params['name_match'], cache=True)
    if vm:
        if (module.params['state'] == 'absent'):
            if module.params['force']:
                pyv.set_powerstate(vm, 'poweredoff', module.params['force'])
            result = pyv.remove_vm(vm)
        elif (module.params['state'] == 'present'):
            result = pyv.reconfigure_vm()
        elif (module.params['state'] in ['poweredon', 'poweredoff', 'restarted', 'suspended']):
            tmp_result = pyv.set_powerstate(vm, module.params['state'], module.params['force'])
            if tmp_result['changed']:
                result['changed'] = True
            if (not tmp_result['failed']):
                result['failed'] = False
        elif (module.params['state'] == 'gatherfacts'):
            try:
                module.exit_json(instance=pyv.gather_facts(vm))
            except Exception:
                e = get_exception()
                module.fail_json(msg=('Fact gather failed with exception %s' % e))
        elif module.params['snapshot_op']:
            result = pyv.snapshot_vm(vm, module.params['name'], module.params['snapshot_op'])
        else:
            assert False
    elif (module.params['state'] in ['poweredon', 'poweredoff', 'present', 'restarted', 'suspended']):
        result = pyv.deploy_vm()
    elif (module.params['state'] == 'gatherfacts'):
        module.fail_json(msg=('Unable to gather facts for non-existing VM %(name)s' % module.params))
    if ('failed' not in result):
        result['failed'] = False
    if result['failed']:
        module.fail_json(**result)
    else:
        module.exit_json(**result)