def snapshot_vm(self, vm, guest, snapshot_op):
    ' To perform snapshot operations create/remove/revert/list_all/list_current/remove_all '
    try:
        snapshot_op_name = snapshot_op['op_type']
    except KeyError:
        self.module.fail_json(msg='Specify op_type - create/remove/revert/list_all/list_current/remove_all')
    task = None
    result = {
        
    }
    if (snapshot_op_name not in ['create', 'remove', 'revert', 'list_all', 'list_current', 'remove_all']):
        self.module.fail_json(msg='Specify op_type - create/remove/revert/list_all/list_current/remove_all')
    if ((snapshot_op_name != 'create') and (vm.snapshot is None)):
        self.module.exit_json(msg=("VM - %s doesn't have any snapshots" % guest))
    if (snapshot_op_name == 'create'):
        try:
            snapname = snapshot_op['name']
        except KeyError:
            self.module.fail_json(msg='specify name & description(optional) to create a snapshot')
        if ('description' in snapshot_op):
            snapdesc = snapshot_op['description']
        else:
            snapdesc = ''
        dumpMemory = False
        quiesce = False
        task = vm.CreateSnapshot(snapname, snapdesc, dumpMemory, quiesce)
    elif (snapshot_op_name in ['remove', 'revert']):
        try:
            snapname = snapshot_op['name']
        except KeyError:
            self.module.fail_json(msg='specify snapshot name')
        snap_obj = self.get_snapshots_by_name_recursively(vm.snapshot.rootSnapshotList, snapname)
        if (len(snap_obj) == 1):
            snap_obj = snap_obj[0].snapshot
            if (snapshot_op_name == 'remove'):
                task = snap_obj.RemoveSnapshot_Task(True)
            else:
                task = snap_obj.RevertToSnapshot_Task()
        else:
            self.module.exit_json(msg=("Couldn't find any snapshots with specified name: %s on VM: %s" % (snapname, guest)))
    elif (snapshot_op_name == 'list_all'):
        snapshot_data = self.list_snapshots_recursively(vm.snapshot.rootSnapshotList)
        result['snapshot_data'] = snapshot_data
    elif (snapshot_op_name == 'list_current'):
        current_snapref = vm.snapshot.currentSnapshot
        current_snap_obj = self.get_current_snap_obj(vm.snapshot.rootSnapshotList, current_snapref)
        result['current_snapshot'] = ('Id: %s; Name: %s; Description: %s; CreateTime: %s; State: %s' % (current_snap_obj[0].id, current_snap_obj[0].name, current_snap_obj[0].description, current_snap_obj[0].createTime, current_snap_obj[0].state))
    elif (snapshot_op_name == 'remove_all'):
        task = vm.RemoveAllSnapshots()
    if task:
        self.wait_for_task(task)
        if (task.info.state == 'error'):
            result = {
                'changed': False,
                'failed': True,
                'msg': task.info.error.msg,
            }
        else:
            result = {
                'changed': True,
                'failed': False,
            }
    return result