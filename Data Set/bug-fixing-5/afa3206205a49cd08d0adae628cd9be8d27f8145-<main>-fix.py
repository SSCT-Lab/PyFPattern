def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(dict(datacenter=dict(type='str'), cluster=dict(type='str'), folder=dict(type='str', default='/vm'), vm_id=dict(type='str', required=True), vm_id_type=dict(default='vm_name', type='str', choices=['inventory_path', 'uuid', 'dns_name', 'vm_name']), vm_username=dict(type='str', required=True), vm_password=dict(type='str', no_log=True, required=True), vm_shell=dict(type='str', required=True), vm_shell_args=dict(default=' ', type='str'), vm_shell_env=dict(type='list'), vm_shell_cwd=dict(type='str')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False, required_if=[['vm_id_type', 'inventory_path', ['folder']]])
    if (not HAS_PYVMOMI):
        module.fail_json(changed=False, msg='pyvmomi is required for this module')
    datacenter_name = module.params['datacenter']
    cluster_name = module.params['cluster']
    folder = module.params['folder']
    content = connect_to_api(module)
    datacenter = None
    if datacenter_name:
        datacenter = find_datacenter_by_name(content, datacenter_name)
        if (not datacenter):
            module.fail_json(changed=False, msg=('Unable to find %(datacenter)s datacenter' % module.params))
    cluster = None
    if cluster_name:
        cluster = find_cluster_by_name(content, cluster_name, datacenter)
        if (not cluster):
            module.fail_json(changed=False, msg=('Unable to find %(cluster)s cluster' % module.params))
    if (module.params['vm_id_type'] == 'inventory_path'):
        vm = find_vm_by_id(content, vm_id=module.params['vm_id'], vm_id_type='inventory_path', folder=folder)
    else:
        vm = find_vm_by_id(content, vm_id=module.params['vm_id'], vm_id_type=module.params['vm_id_type'], datacenter=datacenter, cluster=cluster)
    if (not vm):
        module.fail_json(msg='Unable to find virtual machine.')
    try:
        msg = execute_command(content, vm, module.params)
        module.exit_json(changed=True, uuid=vm.summary.config.uuid, msg=msg)
    except vmodl.RuntimeFault as runtime_fault:
        module.fail_json(changed=False, msg=runtime_fault.msg)
    except vmodl.MethodFault as method_fault:
        module.fail_json(changed=False, msg=method_fault.msg)
    except Exception as e:
        module.fail_json(changed=False, msg=str(e))