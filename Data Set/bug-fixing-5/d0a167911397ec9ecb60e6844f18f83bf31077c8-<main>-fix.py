def main():
    module = AnsibleModule(argument_spec=dict(hostname=dict(type='str', default=os.environ.get('VMWARE_HOST')), username=dict(type='str', default=os.environ.get('VMWARE_USER')), password=dict(type='str', no_log=True, default=os.environ.get('VMWARE_PASSWORD')), validate_certs=dict(required=False, type='bool', default=True), name=dict(required=True, type='str'), name_match=dict(required=False, type='str', default='first'), uuid=dict(required=False, type='str'), folder=dict(required=False, type='str', default='/vm'), datacenter=dict(required=True, type='str')))
    module.params['folder'] = module.params['folder'].rstrip('/')
    pyv = PyVmomiHelper(module)
    vm = pyv.getvm(name=module.params['name'], folder=module.params['folder'], uuid=module.params['uuid'])
    if vm:
        try:
            module.exit_json(instance=pyv.gather_facts(vm))
        except Exception as e:
            module.fail_json(msg=('Fact gather failed with exception %s' % to_native(e)))
    else:
        module.fail_json(msg=('Unable to gather facts for non-existing Virtual Machine %(name)s' % module.params))