def main():
    argument_spec = ovirt_full_argument_spec(state=dict(choices=['present', 'absent', 'attached', 'detached', 'exported'], default='present'), id=dict(default=None), name=dict(default=None, aliases=['alias']), description=dict(default=None), vm_name=dict(default=None), vm_id=dict(default=None), size=dict(default=None), interface=dict(default=None), storage_domain=dict(default=None), storage_domains=dict(default=None, type='list'), profile=dict(default=None), quota_id=dict(default=None), format=dict(default='cow', choices=['raw', 'cow']), sparse=dict(default=None, type='bool'), bootable=dict(default=None, type='bool'), shareable=dict(default=None, type='bool'), logical_unit=dict(default=None, type='dict'), download_image_path=dict(default=None), upload_image_path=dict(default=None, aliases=['image_path']), force=dict(default=False, type='bool'), sparsify=dict(default=None, type='bool'), openstack_volume_type=dict(default=None), image_provider=dict(default=None))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (module._name == 'ovirt_disks'):
        module.deprecate("The 'ovirt_disks' module is being renamed 'ovirt_disk'", version=2.8)
    check_sdk(module)
    check_params(module)
    try:
        disk = None
        state = module.params['state']
        auth = module.params.get('auth')
        connection = create_connection(auth)
        disks_service = connection.system_service().disks_service()
        disks_module = DisksModule(connection=connection, module=module, service=disks_service)
        lun = module.params.get('logical_unit')
        if lun:
            disk = _search_by_lun(disks_service, lun.get('id'))
        ret = None
        if (state in ('present', 'detached', 'attached')):
            ret = disks_module.create(entity=disk, result_state=(otypes.DiskStatus.OK if (lun is None) else None))
            is_new_disk = ret['changed']
            ret['changed'] = (ret['changed'] or disks_module.update_storage_domains(ret['id']))
            module.params['id'] = (ret['id'] if (disk is None) else disk.id)
            if (module.params['upload_image_path'] and (is_new_disk or module.params['force'])):
                uploaded = upload_disk_image(connection, module)
                ret['changed'] = (ret['changed'] or uploaded)
            if (module.params['download_image_path'] and ((not os.path.isfile(module.params['download_image_path'])) or module.params['force'])):
                downloaded = download_disk_image(connection, module)
                ret['changed'] = (ret['changed'] or downloaded)
            disk = disks_service.disk_service(module.params['id']).get()
            if (disk.storage_type == otypes.DiskStorageType.IMAGE):
                ret = disks_module.action(action='sparsify', action_condition=(lambda d: module.params['sparsify']), wait_condition=(lambda d: (d.status == otypes.DiskStatus.OK)))
        elif (state == 'exported'):
            disk = disks_module.search_entity()
            if (disk is None):
                module.fail_json(msg=(("Can not export given disk '%s', it doesn't exist" % module.params.get('name')) or module.params.get('id')))
            if (disk.storage_type == otypes.DiskStorageType.IMAGE):
                ret = disks_module.action(action='export', action_condition=(lambda d: module.params['image_provider']), wait_condition=(lambda d: (d.status == otypes.DiskStatus.OK)), storage_domain=otypes.StorageDomain(name=module.params['image_provider']))
        elif (state == 'absent'):
            ret = disks_module.remove()
        if ((module.params.get('vm_id') is not None) or ((module.params.get('vm_name') is not None) and (state != 'absent'))):
            vms_service = connection.system_service().vms_service()
            vm_id = module.params['vm_id']
            if (vm_id is None):
                vm_id = getattr(search_by_name(vms_service, module.params['vm_name']), 'id', None)
            if (vm_id is None):
                module.fail_json(msg="VM don't exists, please create it first.")
            disk_attachments_service = vms_service.vm_service(vm_id).disk_attachments_service()
            disk_attachments_module = DiskAttachmentsModule(connection=connection, module=module, service=disk_attachments_service, changed=(ret['changed'] if ret else False))
            if ((state == 'present') or (state == 'attached')):
                ret = disk_attachments_module.create()
                if (lun is None):
                    wait(service=disk_attachments_service.service(ret['id']), condition=(lambda d: (follow_link(connection, d.disk).status == otypes.DiskStatus.OK)), wait=module.params['wait'], timeout=module.params['timeout'])
            elif (state == 'detached'):
                ret = disk_attachments_module.remove()
        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))