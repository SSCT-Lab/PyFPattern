def rename_snapshot(self, vm):
    if (vm.snapshot is None):
        self.module.fail_json(msg=("virtual machine - %s doesn't have any snapshots" % (self.module.params.get('uuid') or self.module.params.get('name'))))
    snap_obj = self.get_snapshots_by_name_recursively(vm.snapshot.rootSnapshotList, self.module.params['snapshot_name'])
    task = None
    if (len(snap_obj) == 1):
        snap_obj = snap_obj[0].snapshot
        if (self.module.params['new_snapshot_name'] and self.module.params['new_description']):
            task = snap_obj.RenameSnapshot(name=self.module.params['new_snapshot_name'], description=self.module.params['new_description'])
        elif self.module.params['new_snapshot_name']:
            task = snap_obj.RenameSnapshot(name=self.module.params['new_snapshot_name'])
        else:
            task = snap_obj.RenameSnapshot(description=self.module.params['new_description'])
    else:
        self.module.exit_json(msg=("Couldn't find any snapshots with specified name: %s on VM: %s" % (self.module.params['snapshot_name'], (self.module.params.get('uuid') or self.module.params.get('name')))))
    return task