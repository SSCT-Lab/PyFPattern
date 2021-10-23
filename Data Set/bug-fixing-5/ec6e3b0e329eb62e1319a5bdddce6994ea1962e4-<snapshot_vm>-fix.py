def snapshot_vm(self, vm):
    memory_dump = False
    quiesce = False
    if vm.capability.quiescedSnapshotsSupported:
        quiesce = self.module.params['quiesce']
    if vm.capability.memorySnapshotsSupported:
        memory_dump = self.module.params['memory_dump']
    task = None
    try:
        task = vm.CreateSnapshot(self.module.params['snapshot_name'], self.module.params['description'], memory_dump, quiesce)
    except vim.fault.RestrictedVersion as exc:
        self.module.fail_json(msg=('Failed to take snapshot due to VMware Licence: %s' % to_native(exc.msg)))
    except Exception as exc:
        self.module.fail_json(msg=('Failed to create snapshot of VM %s due to %s' % (self.module.params['name'], to_native(exc.msg))))
    return task