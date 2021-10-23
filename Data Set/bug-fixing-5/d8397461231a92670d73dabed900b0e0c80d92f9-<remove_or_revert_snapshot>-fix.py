def remove_or_revert_snapshot(self, vm):
    if (vm.snapshot is None):
        vm_name = (self.module.params.get('uuid') or self.module.params.get('name'))
        if (self.module.params.get('state') == 'revert'):
            self.module.fail_json(msg=('virtual machine - %s does not have any snapshots to revert to.' % vm_name))
        self.module.exit_json(msg=("virtual machine - %s doesn't have any snapshots to remove." % vm_name))
    snap_obj = self.get_snapshots_by_name_recursively(vm.snapshot.rootSnapshotList, self.module.params['snapshot_name'])
    task = None
    if (len(snap_obj) == 1):
        snap_obj = snap_obj[0].snapshot
        if (self.module.params['state'] == 'absent'):
            remove_children = self.module.params.get('remove_children', False)
            task = snap_obj.RemoveSnapshot_Task(remove_children)
        elif (self.module.params['state'] == 'revert'):
            task = snap_obj.RevertToSnapshot_Task()
    else:
        self.module.exit_json(msg=("Couldn't find any snapshots with specified name: %s on VM: %s" % (self.module.params['snapshot_name'], (self.module.params.get('uuid') or self.module.params.get('name')))))
    return task