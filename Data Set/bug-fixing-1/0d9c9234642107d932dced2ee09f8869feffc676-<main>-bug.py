

def main():
    argument_spec = ovirt_full_argument_spec(state=dict(type='str', default='present', choices=['absent', 'next_run', 'present', 'registered', 'running', 'stopped', 'suspended', 'exported']), name=dict(type='str'), id=dict(type='str'), cluster=dict(type='str'), allow_partial_import=dict(type='bool'), template=dict(type='str'), template_version=dict(type='int'), use_latest_template_version=dict(type='bool'), storage_domain=dict(type='str'), disk_format=dict(type='str', default='cow', choices=['cow', 'raw']), disks=dict(type='list', default=[]), memory=dict(type='str'), memory_guaranteed=dict(type='str'), memory_max=dict(type='str'), cpu_sockets=dict(type='int'), cpu_cores=dict(type='int'), cpu_shares=dict(type='int'), cpu_threads=dict(type='int'), type=dict(type='str', choices=['server', 'desktop', 'high_performance']), operating_system=dict(type='str'), cd_iso=dict(type='str'), boot_devices=dict(type='list', choices=['cdrom', 'hd', 'network']), vnic_profile_mappings=dict(default=[], type='list'), cluster_mappings=dict(default=[], type='list'), role_mappings=dict(default=[], type='list'), affinity_group_mappings=dict(default=[], type='list'), affinity_label_mappings=dict(default=[], type='list'), lun_mappings=dict(default=[], type='list'), domain_mappings=dict(default=[], type='list'), reassign_bad_macs=dict(default=None, type='bool'), boot_menu=dict(type='bool'), serial_console=dict(type='bool'), usb_support=dict(type='bool'), sso=dict(type='bool'), quota_id=dict(type='str'), high_availability=dict(type='bool'), high_availability_priority=dict(type='int'), lease=dict(type='str'), stateless=dict(type='bool'), delete_protected=dict(type='bool'), force=dict(type='bool', default=False), nics=dict(type='list', default=[]), cloud_init=dict(type='dict'), cloud_init_nics=dict(type='list', default=[]), cloud_init_persist=dict(type='bool', default=False, aliases=['sysprep_persist']), kernel_params_persist=dict(type='bool', default=False), sysprep=dict(type='dict'), host=dict(type='str'), clone=dict(type='bool', default=False), clone_permissions=dict(type='bool', default=False), kernel_path=dict(type='str'), initrd_path=dict(type='str'), kernel_params=dict(type='str'), instance_type=dict(type='str'), description=dict(type='str'), comment=dict(type='str'), timezone=dict(type='str'), serial_policy=dict(type='str', choices=['vm', 'host', 'custom']), serial_policy_value=dict(type='str'), vmware=dict(type='dict'), xen=dict(type='dict'), kvm=dict(type='dict'), cpu_mode=dict(type='str'), placement_policy=dict(type='str'), custom_compatibility_version=dict(type='str'), ticket=dict(type='bool', default=None), cpu_pinning=dict(type='list'), soundcard_enabled=dict(type='bool', default=None), smartcard_enabled=dict(type='bool', default=None), io_threads=dict(type='int', default=None), ballooning_enabled=dict(type='bool', default=None), rng_device=dict(type='str'), numa_tune_mode=dict(type='str', choices=['interleave', 'preferred', 'strict']), numa_nodes=dict(type='list', default=[]), custom_properties=dict(type='list'), watchdog=dict(type='dict'), host_devices=dict(type='list'), graphical_console=dict(type='dict'), exclusive=dict(type='bool'), export_domain=dict(default=None), export_ova=dict(type='dict'), force_migrate=dict(type='bool'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_one_of=[['id', 'name']])
    check_sdk(module)
    check_params(module)
    try:
        state = module.params['state']
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        vms_service = connection.system_service().vms_service()
        vms_module = VmsModule(connection=connection, module=module, service=vms_service)
        vm = vms_module.search_entity(list_params={
            'all_content': True,
        })
        control_state(vm, vms_service, module)
        if (state in ('present', 'running', 'next_run')):
            if (module.params['xen'] or module.params['kvm'] or module.params['vmware']):
                vms_module.changed = import_vm(module, connection)
            ret = vms_module.create(entity=vm, result_state=(otypes.VmStatus.DOWN if (vm is None) else None), clone=module.params['clone'], clone_permissions=module.params['clone_permissions'])
            if (module.check_mode and (ret.get('id') is None)):
                module.exit_json(**ret)
            vms_module.post_present(ret['id'])
            if (state == 'running'):

                def kernel_persist_check():
                    return (module.params.get('kernel_params') or module.params.get('initrd_path') or (module.params.get('kernel_path') and (not module.params.get('cloud_init_persist'))))
                initialization = vms_module.get_initialization()
                ret = vms_module.action(action='start', post_action=vms_module._post_start_action, action_condition=(lambda vm: (vm.status not in [otypes.VmStatus.MIGRATING, otypes.VmStatus.POWERING_UP, otypes.VmStatus.REBOOT_IN_PROGRESS, otypes.VmStatus.WAIT_FOR_LAUNCH, otypes.VmStatus.UP, otypes.VmStatus.RESTORING_STATE])), wait_condition=(lambda vm: (vm.status == otypes.VmStatus.UP)), use_cloud_init=(True if ((not module.params.get('cloud_init_persist')) and (module.params.get('cloud_init') is not None)) else None), use_sysprep=(True if ((not module.params.get('cloud_init_persist')) and (module.params.get('sysprep') is not None)) else None), vm=(otypes.Vm(placement_policy=(otypes.VmPlacementPolicy(hosts=[otypes.Host(name=module.params['host'])]) if module.params['host'] else None), initialization=initialization, os=(otypes.OperatingSystem(cmdline=module.params.get('kernel_params'), initrd=module.params.get('initrd_path'), kernel=module.params.get('kernel_path')) if kernel_persist_check() else None)) if (kernel_persist_check() or module.params.get('host') or ((initialization is not None) and (not module.params.get('cloud_init_persist')))) else None))
                if module.params['ticket']:
                    vm_service = vms_service.vm_service(ret['id'])
                    graphics_consoles_service = vm_service.graphics_consoles_service()
                    graphics_console = graphics_consoles_service.list()[0]
                    console_service = graphics_consoles_service.console_service(graphics_console.id)
                    ticket = console_service.remote_viewer_connection_file()
                    if ticket:
                        ret['vm']['remote_vv_file'] = ticket
            if (state == 'next_run'):
                vm = vms_service.vm_service(ret['id']).get()
                if vm.next_run_configuration_exists:
                    ret = vms_module.action(action='reboot', entity=vm, action_condition=(lambda vm: (vm.status == otypes.VmStatus.UP)), wait_condition=(lambda vm: (vm.status == otypes.VmStatus.UP)))
            ret['changed'] = vms_module.changed
        elif (state == 'stopped'):
            if (module.params['xen'] or module.params['kvm'] or module.params['vmware']):
                vms_module.changed = import_vm(module, connection)
            ret = vms_module.create(entity=vm, result_state=(otypes.VmStatus.DOWN if (vm is None) else None), clone=module.params['clone'], clone_permissions=module.params['clone_permissions'])
            if module.params['force']:
                ret = vms_module.action(action='stop', action_condition=(lambda vm: (vm.status != otypes.VmStatus.DOWN)), wait_condition=vms_module.wait_for_down)
            else:
                ret = vms_module.action(action='shutdown', pre_action=vms_module._pre_shutdown_action, action_condition=(lambda vm: (vm.status != otypes.VmStatus.DOWN)), wait_condition=vms_module.wait_for_down)
            vms_module.post_present(ret['id'])
        elif (state == 'suspended'):
            ret = vms_module.create(entity=vm, result_state=(otypes.VmStatus.DOWN if (vm is None) else None), clone=module.params['clone'], clone_permissions=module.params['clone_permissions'])
            vms_module.post_present(ret['id'])
            ret = vms_module.action(action='suspend', pre_action=vms_module._pre_suspend_action, action_condition=(lambda vm: (vm.status != otypes.VmStatus.SUSPENDED)), wait_condition=(lambda vm: (vm.status == otypes.VmStatus.SUSPENDED)))
        elif (state == 'absent'):
            ret = vms_module.remove()
        elif (state == 'registered'):
            storage_domains_service = connection.system_service().storage_domains_service()
            sd_id = get_id_by_name(storage_domains_service, module.params['storage_domain'])
            storage_domain_service = storage_domains_service.storage_domain_service(sd_id)
            vms_service = storage_domain_service.vms_service()
            vms = vms_service.list(unregistered=True)
            vm = next((vm for vm in vms if ((vm.id == module.params['id']) or (vm.name == module.params['name']))), None)
            changed = False
            if (vm is None):
                vm = vms_module.search_entity()
                if (vm is None):
                    raise ValueError(("VM '%s(%s)' wasn't found." % (module.params['name'], module.params['id'])))
            else:
                changed = True
                vm_service = vms_service.vm_service(vm.id)
                vm_service.register(allow_partial_import=module.params['allow_partial_import'], cluster=(otypes.Cluster(name=module.params['cluster']) if module.params['cluster'] else None), vnic_profile_mappings=(_get_vnic_profile_mappings(module) if module.params['vnic_profile_mappings'] else None), reassign_bad_macs=(module.params['reassign_bad_macs'] if (module.params['reassign_bad_macs'] is not None) else None), registration_configuration=(otypes.RegistrationConfiguration(cluster_mappings=_get_cluster_mappings(module), role_mappings=_get_role_mappings(module), domain_mappings=_get_domain_mappings(module), lun_mappings=_get_lun_mappings(module), affinity_group_mappings=_get_affinity_group_mappings(module), affinity_label_mappings=_get_affinity_label_mappings(module)) if (module.params['cluster_mappings'] or module.params['role_mappings'] or module.params['domain_mappings'] or module.params['lun_mappings'] or module.params['affinity_group_mappings'] or module.params['affinity_label_mappings']) else None))
                if module.params['wait']:
                    vm = vms_module.wait_for_import()
                else:
                    vm = vm_service.get()
            ret = {
                'changed': changed,
                'id': vm.id,
                'vm': get_dict_of_struct(vm),
            }
        elif (state == 'exported'):
            if module.params['export_domain']:
                export_service = vms_module._get_export_domain_service()
                export_vm = search_by_attributes(export_service.vms_service(), id=vm.id)
                ret = vms_module.action(entity=vm, action='export', action_condition=(lambda t: ((export_vm is None) or module.params['exclusive'])), wait_condition=(lambda t: (t is not None)), post_action=vms_module.post_export_action, storage_domain=otypes.StorageDomain(id=export_service.get().id), exclusive=module.params['exclusive'])
            elif module.params['export_ova']:
                export_vm = module.params['export_ova']
                ret = vms_module.action(entity=vm, action='export_to_path_on_host', host=otypes.Host(name=export_vm.get('host')), directory=export_vm.get('directory'), filename=export_vm.get('filename'))
        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))
