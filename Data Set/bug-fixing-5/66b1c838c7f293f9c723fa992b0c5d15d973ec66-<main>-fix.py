def main():
    argument_spec = ovirt_full_argument_spec(state=dict(choices=['restore', 'present', 'absent'], default='present'), vm_name=dict(required=True), snapshot_id=dict(default=None), description=dict(default=None), keep_days_old=dict(default=None, type='int'), use_memory=dict(default=None, type='bool', aliases=['restore_memory', 'save_memory']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[('state', 'absent', ['snapshot_id']), ('state', 'restore', ['snapshot_id'])])
    check_sdk(module)
    vm_name = module.params.get('vm_name')
    auth = module.params.pop('auth')
    connection = create_connection(auth)
    vms_service = connection.system_service().vms_service()
    vm = search_by_name(vms_service, vm_name)
    if (not vm):
        module.fail_json(msg="Vm '{name}' doesn't exist.".format(name=vm_name))
    vm_service = vms_service.vm_service(vm.id)
    snapshots_service = vms_service.vm_service(vm.id).snapshots_service()
    try:
        state = module.params['state']
        if (state == 'present'):
            if (module.params.get('keep_days_old') is not None):
                ret = remove_old_snapshosts(module, vm_service, snapshots_service)
            else:
                ret = create_snapshot(module, vm_service, snapshots_service)
        elif (state == 'restore'):
            ret = restore_snapshot(module, vm_service, snapshots_service)
        elif (state == 'absent'):
            ret = remove_snapshot(module, vm_service, snapshots_service)
        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))