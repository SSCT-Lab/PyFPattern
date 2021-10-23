def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(dict(datacenter=dict(default=None, type='str'), cluster=dict(default=None, type='str'), folder=dict(type='str', default='/vm'), vm_id=dict(required=True, type='str'), vm_id_type=dict(default='vm_name', type='str', choices=['inventory_path', 'uuid', 'dns_name', 'vm_name']), vm_username=dict(required=False, type='str'), vm_password=dict(required=False, type='str', no_log=True), vm_shell=dict(required=True, type='str'), vm_shell_args=dict(default=' ', type='str'), vm_shell_env=dict(default=None, type='list'), vm_shell_cwd=dict(default=None, type='str')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False, required_if=[['vm_id_type', 'inventory_path', ['folder']]])
    if (not HAS_PYVMOMI):
        module.fail_json(changed=False, msg='pyvmomi is required for this module')
    try:
        p = module.params
        datacenter_name = p['datacenter']
        cluster_name = p['cluster']
        folder = p['folder']
        content = connect_to_api(module)
        datacenter = None
        if datacenter_name:
            datacenter = find_datacenter_by_name(content, datacenter_name)
            if (not datacenter):
                module.fail_json(changed=False, msg='datacenter not found')
        cluster = None
        if cluster_name:
            cluster = find_cluster_by_name(content, cluster_name, datacenter)
            if (not cluster):
                module.fail_json(changed=False, msg='cluster not found')
        if (p['vm_id_type'] == 'inventory_path'):
            vm = find_vm_by_id(content, vm_id=p['vm_id'], vm_id_type='inventory_path', folder=folder)
        else:
            vm = find_vm_by_id(content, vm_id=p['vm_id'], vm_id_type=p['vm_id_type'], datacenter=datacenter, cluster=cluster)
        if (not vm):
            module.fail_json(msg='VM not found')
        msg = execute_command(content, vm, p['vm_username'], p['vm_password'], p['vm_shell'], p['vm_shell_args'], p['vm_shell_env'], p['vm_shell_cwd'])
        module.exit_json(changed=True, uuid=vm.summary.config.uuid, msg=msg)
    except vmodl.RuntimeFault as runtime_fault:
        module.fail_json(changed=False, msg=runtime_fault.msg)
    except vmodl.MethodFault as method_fault:
        module.fail_json(changed=False, msg=method_fault.msg)
    except Exception as e:
        module.fail_json(changed=False, msg=str(e))