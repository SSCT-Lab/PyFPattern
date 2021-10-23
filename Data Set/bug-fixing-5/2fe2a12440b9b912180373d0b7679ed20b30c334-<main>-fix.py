def main():
    argument_spec = ovirt_full_argument_spec(state=dict(choices=['present', 'absent', 'attached', 'detached', 'exported', 'imported'], default='present'), id=dict(default=None), name=dict(default=None, aliases=['alias']), description=dict(default=None), vm_name=dict(default=None), vm_id=dict(default=None), size=dict(default=None), interface=dict(default=None), storage_domain=dict(default=None), storage_domains=dict(default=None, type='list'), profile=dict(default=None), quota_id=dict(default=None), format=dict(default='cow', choices=['raw', 'cow']), content_type=dict(default='data', choices=['data', 'iso', 'hosted_engine', 'hosted_engine_sanlock', 'hosted_engine_metadata', 'hosted_engine_configuration']), sparse=dict(default=None, type='bool'), bootable=dict(default=None, type='bool'), shareable=dict(default=None, type='bool'), logical_unit=dict(default=None, type='dict'), download_image_path=dict(default=None), upload_image_path=dict(default=None, aliases=['image_path']), force=dict(default=False, type='bool'), sparsify=dict(default=None, type='bool'), openstack_volume_type=dict(default=None), image_provider=dict(default=None), host=dict(default=None), wipe_after_delete=dict(type='bool', default=None), activate=dict(default=None, type='bool'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    lun = module.params.get('logical_unit')
    host = module.params['host']
    if ((host and (lun is None)) or (host and (lun.get('id') is None))):
        module.fail_json(msg='Can not use parameter host ({0!s}) without specifying the logical_unit id'.format(host))
    check_sdk(module)
    check_params(module)
    try:
        disk = None
        state = module.params['state']
        auth = module.params.get('auth')
        connection = create_connection(auth)
        disks_service = connection.system_service().disks_service()
        disks_module = DisksModule(connection=connection, module=module, service=disks_service)
        force_create = False
        vm_service = get_vm_service(connection, module)
        if lun:
            disk = _search_by_lun(disks_service, lun.get('id'))
        else:
            disk = disks_module.search_entity(search_params=searchable_attributes(module))
            if (vm_service and disk):
                force_create = (disk.id not in [a.disk.id for a in vm_service.disk_attachments_service().list() if a.disk])
        ret = None
        if (state in ('present', 'detached', 'attached')):
            if ((vm_service is not None) and (disk is None)):
                module.params['activate'] = True
            ret = disks_module.create(entity=(disk if (not force_create) else None), result_state=(otypes.DiskStatus.OK if (lun is None) else None), fail_condition=(lambda d: ((d.status == otypes.DiskStatus.ILLEGAL) if (lun is None) else False)), force_create=force_create)
            is_new_disk = ret['changed']
            ret['changed'] = (ret['changed'] or disks_module.update_storage_domains(ret['id']))
            module.params['id'] = ret['id']
            if (module.params['upload_image_path'] and (is_new_disk or module.params['force'])):
                uploaded = upload_disk_image(connection, module)
                ret['changed'] = (ret['changed'] or uploaded)
            if (module.params['download_image_path'] and ((not os.path.isfile(module.params['download_image_path'])) or module.params['force'])):
                downloaded = download_disk_image(connection, module)
                ret['changed'] = (ret['changed'] or downloaded)
            if (not module.check_mode):
                disk = disks_service.disk_service(module.params['id']).get()
                if (disk.storage_type == otypes.DiskStorageType.IMAGE):
                    ret = disks_module.action(action='sparsify', action_condition=(lambda d: module.params['sparsify']), wait_condition=(lambda d: (d.status == otypes.DiskStatus.OK)))
        elif (state == 'exported'):
            disk = disks_module.search_entity()
            if (disk is None):
                module.fail_json(msg=(("Can not export given disk '%s', it doesn't exist" % module.params.get('name')) or module.params.get('id')))
            if (disk.storage_type == otypes.DiskStorageType.IMAGE):
                ret = disks_module.action(action='export', action_condition=(lambda d: module.params['image_provider']), wait_condition=(lambda d: (d.status == otypes.DiskStatus.OK)), storage_domain=otypes.StorageDomain(name=module.params['image_provider']))
        elif (state == 'imported'):
            glance_service = connection.system_service().openstack_image_providers_service()
            image_provider = search_by_name(glance_service, module.params['image_provider'])
            images_service = glance_service.service(image_provider.id).images_service()
            entity_id = get_id_by_name(images_service, module.params['name'])
            images_service.service(entity_id).import_(storage_domain=(otypes.StorageDomain(name=module.params['storage_domain']) if module.params['storage_domain'] else None), disk=otypes.Disk(name=module.params['name']), import_as_template=False)
            disk = disks_module.wait_for_import(condition=(lambda t: (t.status == otypes.DiskStatus.OK)))
            ret = disks_module.create(result_state=otypes.DiskStatus.OK)
        elif (state == 'absent'):
            ret = disks_module.remove()
        if vm_service:
            disk_attachments_service = vm_service.disk_attachments_service()
            disk_attachments_module = DiskAttachmentsModule(connection=connection, module=module, service=disk_attachments_service, changed=(ret['changed'] if ret else False))
            if ((state == 'present') or (state == 'attached')):
                ret = disk_attachments_module.create()
                if (lun is None):
                    wait(service=disk_attachments_service.service(ret['id']), condition=(lambda d: (follow_link(connection, d.disk).status == otypes.DiskStatus.OK)), wait=module.params['wait'], timeout=module.params['timeout'])
            elif (state == 'detached'):
                ret = disk_attachments_module.remove()
        if ((state != 'absent') and host):
            hosts_service = connection.system_service().hosts_service()
            host_id = get_id_by_name(hosts_service, host)
            disks_service.disk_service(disk.id).refresh_lun(otypes.Host(id=host_id))
        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))