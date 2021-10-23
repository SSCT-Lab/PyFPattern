def main():
    argument_spec = ovirt_full_argument_spec(state=dict(choices=['running', 'stopped', 'present', 'absent', 'suspended', 'next_run'], default='present'), name=dict(default=None), id=dict(default=None), cluster=dict(default=None), template=dict(default=None), template_version=dict(default=None, type='int'), use_latest_template_version=dict(default=None, type='bool'), disks=dict(default=[], type='list'), memory=dict(default=None), memory_guaranteed=dict(default=None), cpu_sockets=dict(default=None, type='int'), cpu_cores=dict(default=None, type='int'), cpu_shares=dict(default=None, type='int'), type=dict(choices=['server', 'desktop']), operating_system=dict(default=None, choices=['rhel_6_ppc64', 'other', 'freebsd', 'windows_2003x64', 'windows_10', 'rhel_6x64', 'rhel_4x64', 'windows_2008x64', 'windows_2008R2x64', 'debian_7', 'windows_2012x64', 'ubuntu_14_04', 'ubuntu_12_04', 'ubuntu_13_10', 'windows_8x64', 'other_linux_ppc64', 'windows_2003', 'other_linux', 'windows_10x64', 'windows_2008', 'rhel_3', 'rhel_5', 'rhel_4', 'other_ppc64', 'sles_11', 'rhel_6', 'windows_xp', 'rhel_7x64', 'freebsdx64', 'rhel_7_ppc64', 'windows_7', 'rhel_5x64', 'ubuntu_14_04_ppc64', 'sles_11_ppc64', 'windows_8', 'windows_2012R2x64', 'windows_2008r2x64', 'ubuntu_13_04', 'ubuntu_12_10', 'windows_7x64']), cd_iso=dict(default=None), boot_devices=dict(default=None, type='list'), high_availability=dict(type='bool'), stateless=dict(type='bool'), delete_protected=dict(type='bool'), force=dict(type='bool', default=False), nics=dict(default=[], type='list'), cloud_init=dict(type='dict'), cloud_init_nics=dict(defaul=[], type='list'), sysprep=dict(type='dict'), host=dict(default=None), clone=dict(type='bool', default=False), clone_permissions=dict(type='bool', default=False), kernel_path=dict(default=None), initrd_path=dict(default=None), kernel_params=dict(default=None), instance_type=dict(default=None), description=dict(default=None), comment=dict(default=None), timezone=dict(default=None), serial_policy=dict(default=None, choices=['vm', 'host', 'custom']), serial_policy_value=dict(default=None))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    check_sdk(module)
    check_params(module)
    try:
        state = module.params['state']
        connection = create_connection(module.params.pop('auth'))
        vms_service = connection.system_service().vms_service()
        vms_module = VmsModule(connection=connection, module=module, service=vms_service)
        vm = vms_module.search_entity()
        control_state(vm, vms_service, module)
        if ((state == 'present') or (state == 'running') or (state == 'next_run')):
            sysprep = module.params['sysprep']
            cloud_init = module.params['cloud_init']
            cloud_init_nics = (module.params['cloud_init_nics'] or [])
            if (cloud_init is not None):
                cloud_init_nics.append(cloud_init)
            vms_module.create(entity=vm, result_state=(otypes.VmStatus.DOWN if (vm is None) else None), clone=module.params['clone'], clone_permissions=module.params['clone_permissions'])
            initialization = _get_initialization(sysprep, cloud_init, cloud_init_nics)
            ret = vms_module.action(action='start', post_action=vms_module._post_start_action, action_condition=(lambda vm: (vm.status not in [otypes.VmStatus.MIGRATING, otypes.VmStatus.POWERING_UP, otypes.VmStatus.REBOOT_IN_PROGRESS, otypes.VmStatus.WAIT_FOR_LAUNCH, otypes.VmStatus.UP, otypes.VmStatus.RESTORING_STATE])), wait_condition=(lambda vm: (vm.status == otypes.VmStatus.UP)), use_cloud_init=((cloud_init is not None) or (len(cloud_init_nics) > 0)), use_sysprep=(sysprep is not None), vm=(otypes.Vm(placement_policy=(otypes.VmPlacementPolicy(hosts=[otypes.Host(name=module.params['host'])]) if module.params['host'] else None), initialization=initialization, os=(otypes.OperatingSystem(cmdline=module.params.get('kernel_params'), initrd=module.params.get('initrd_path'), kernel=module.params.get('kernel_path')) if (module.params.get('kernel_params') or module.params.get('initrd_path') or module.params.get('kernel_path')) else None)) if (module.params.get('kernel_params') or module.params.get('initrd_path') or module.params.get('kernel_path') or module.params.get('host') or initialization) else None))
            if (state == 'next_run'):
                vm = vms_service.vm_service(ret['id']).get()
                if vm.next_run_configuration_exists:
                    ret = vms_module.action(action='reboot', entity=vm, action_condition=(lambda vm: (vm.status == otypes.VmStatus.UP)), wait_condition=(lambda vm: (vm.status == otypes.VmStatus.UP)))
        elif (state == 'stopped'):
            vms_module.create(result_state=(otypes.VmStatus.DOWN if (vm is None) else None), clone=module.params['clone'], clone_permissions=module.params['clone_permissions'])
            if module.params['force']:
                ret = vms_module.action(action='stop', post_action=vms_module._attach_cd, action_condition=(lambda vm: (vm.status != otypes.VmStatus.DOWN)), wait_condition=vms_module.wait_for_down)
            else:
                ret = vms_module.action(action='shutdown', pre_action=vms_module._pre_shutdown_action, post_action=vms_module._attach_cd, action_condition=(lambda vm: (vm.status != otypes.VmStatus.DOWN)), wait_condition=vms_module.wait_for_down)
        elif (state == 'suspended'):
            vms_module.create(result_state=(otypes.VmStatus.DOWN if (vm is None) else None), clone=module.params['clone'], clone_permissions=module.params['clone_permissions'])
            ret = vms_module.action(action='suspend', pre_action=vms_module._pre_suspend_action, action_condition=(lambda vm: (vm.status != otypes.VmStatus.SUSPENDED)), wait_condition=(lambda vm: (vm.status == otypes.VmStatus.SUSPENDED)))
        elif (state == 'absent'):
            ret = vms_module.remove()
        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=False)