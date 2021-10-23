def create_snapshot(module, vm_service, snapshots_service, connection):
    changed = False
    snapshot = get_entity(snapshots_service.snapshot_service(module.params['snapshot_id']))
    if (snapshot is None):
        if (not module.check_mode):
            disk_attachments_id = (set((get_disk_attachment(disk, vm_service.disk_attachments_service().list(), connection).id for disk in module.params.get('disks'))) if module.params.get('disks') else None)
            snapshot = snapshots_service.add(otypes.Snapshot(description=module.params.get('description'), persist_memorystate=module.params.get('use_memory'), disk_attachments=([otypes.DiskAttachment(id=da_id) for da_id in disk_attachments_id] if disk_attachments_id else None)))
        changed = True
        wait(service=snapshots_service.snapshot_service(snapshot.id), condition=(lambda snap: (snap.snapshot_status == otypes.SnapshotStatus.OK)), wait=module.params['wait'], timeout=module.params['timeout'])
    return {
        'changed': changed,
        'id': snapshot.id,
        'snapshot': get_dict_of_struct(snapshot),
    }