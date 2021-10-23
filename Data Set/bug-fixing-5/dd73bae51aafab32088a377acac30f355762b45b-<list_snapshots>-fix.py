def list_snapshots(vm):
    result = {
        
    }
    snapshot = _get_vm_prop(vm, ('snapshot',))
    if (not snapshot):
        return result
    if (vm.snapshot is None):
        return result
    result['snapshots'] = list_snapshots_recursively(vm.snapshot.rootSnapshotList)
    current_snapref = vm.snapshot.currentSnapshot
    current_snap_obj = get_current_snap_obj(vm.snapshot.rootSnapshotList, current_snapref)
    if current_snap_obj:
        result['current_snapshot'] = deserialize_snapshot_obj(current_snap_obj[0])
    else:
        result['current_snapshot'] = dict()
    return result