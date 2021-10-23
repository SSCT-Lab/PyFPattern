def create_snapshot(module, vm_service, snapshots_service):
    changed = False
    snapshot = get_entity(snapshots_service.snapshot_service(module.params['snapshot_id']))
    if (snapshot is None):
        if (not module.check_mode):
            snapshot = snapshots_service.add(otypes.Snapshot(description=module.params.get('description'), persist_memorystate=module.params.get('use_memory')))
        changed = True
        wait(service=snapshots_service.snapshot_service(snapshot.id), condition=(lambda snap: (snap.snapshot_status == otypes.SnapshotStatus.OK)), wait=module.params['wait'], timeout=module.params['timeout'])
    return {
        'changed': changed,
        'id': snapshot.id,
        'snapshot': get_dict_of_struct(snapshot),
    }