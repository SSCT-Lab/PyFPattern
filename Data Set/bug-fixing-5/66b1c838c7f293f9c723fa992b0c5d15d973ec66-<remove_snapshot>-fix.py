def remove_snapshot(module, vm_service, snapshots_service, snapshot_id=None):
    changed = False
    if (not snapshot_id):
        snapshot_id = module.params['snapshot_id']
    snapshot = get_entity(snapshots_service.snapshot_service(snapshot_id))
    if snapshot:
        snapshot_service = snapshots_service.snapshot_service(snapshot.id)
        if (not module.check_mode):
            snapshot_service.remove()
        changed = True
        wait(service=snapshot_service, condition=(lambda snapshot: (snapshot is None)), wait=module.params['wait'], timeout=module.params['timeout'])
    return {
        'changed': changed,
        'id': (snapshot.id if snapshot else None),
        'snapshot': get_dict_of_struct(snapshot),
    }