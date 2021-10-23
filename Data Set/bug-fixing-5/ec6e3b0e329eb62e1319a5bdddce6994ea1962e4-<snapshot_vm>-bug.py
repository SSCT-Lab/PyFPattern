def snapshot_vm(self, vm):
    memory_dump = False
    quiesce = False
    if vm.capability.quiescedSnapshotsSupported:
        quiesce = self.module.params['quiesce']
    if vm.capability.memorySnapshotsSupported:
        memory_dump = self.module.params['memory_dump']
    return vm.CreateSnapshot(self.module.params['snapshot_name'], self.module.params['description'], memory_dump, quiesce)