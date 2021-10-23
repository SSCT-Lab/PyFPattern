def main():
    module = AnsibleModule(argument_spec=dict(hostname=dict(type='str', default=os.environ.get('VMWARE_HOST')), username=dict(type='str', default=os.environ.get('VMWARE_USER')), password=dict(type='str', no_log=True, default=os.environ.get('VMWARE_PASSWORD')), state=dict(required=False, choices=['poweredon', 'poweredoff', 'present', 'absent', 'restarted', 'suspended', 'shutdownguest', 'rebootguest'], default='present'), validate_certs=dict(type='bool', default=True), template_src=dict(type='str', aliases=['template']), is_template=dict(type='bool', default=False), annotation=dict(type='str', aliases=['notes']), customvalues=dict(type='list', default=[]), name=dict(required=True, type='str'), name_match=dict(type='str', default='first'), uuid=dict(type='str'), folder=dict(type='str', default='/vm'), guest_id=dict(type='str'), disk=dict(type='list', default=[]), hardware=dict(type='dict', default={
        
    }), force=dict(type='bool', default=False), datacenter=dict(type='str', default='ha-datacenter'), esxi_hostname=dict(type='str'), cluster=dict(type='str'), wait_for_ip_address=dict(type='bool', default=False), networks=dict(type='list', default=[]), resource_pool=dict(type='str'), customization=dict(type='dict', no_log=True, default={
        
    })), supports_check_mode=True, mutually_exclusive=[['esxi_hostname', 'cluster']], required_together=[['state', 'force'], ['template']])
    result = {
        'failed': False,
        'changed': False,
    }
    if ((not module.params['folder'].startswith('/vm')) and module.params['folder'].startswith('/')):
        module.params['folder'] = ('/vm%(folder)s' % module.params)
    module.params['folder'] = module.params['folder'].rstrip('/')
    pyv = PyVmomiHelper(module)
    vm = pyv.getvm(name=module.params['name'], folder=module.params['folder'], uuid=module.params['uuid'])
    if vm:
        if (module.params['state'] == 'absent'):
            if module.params['force']:
                pyv.set_powerstate(vm, 'poweredoff', module.params['force'])
            result = pyv.remove_vm(vm)
        elif (module.params['state'] == 'present'):
            result = pyv.reconfigure_vm()
        elif (module.params['state'] in ['poweredon', 'poweredoff', 'restarted', 'suspended', 'shutdownguest', 'rebootguest']):
            tmp_result = pyv.set_powerstate(vm, module.params['state'], module.params['force'])
            if tmp_result['changed']:
                result['changed'] = True
            if (not tmp_result['failed']):
                result['failed'] = False
        else:
            assert False
    elif (module.params['state'] in ['poweredon', 'poweredoff', 'present', 'restarted', 'suspended']):
        result = pyv.deploy_vm()
    if ('failed' not in result):
        result['failed'] = False
    if result['failed']:
        module.fail_json(**result)
    else:
        module.exit_json(**result)