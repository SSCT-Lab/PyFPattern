def wait_for_down(self, vm):
    "\n        This function will first wait for the status DOWN of the VM.\n        Then it will find the active snapshot and wait until it's state is OK for\n        stateless VMs and statless snaphot is removed.\n        "
    vm_service = self._service.vm_service(vm.id)
    wait(service=vm_service, condition=(lambda vm: (vm.status == otypes.VmStatus.DOWN)), wait=self.param('wait'), timeout=self.param('timeout'))
    if vm.stateless:
        snapshots_service = vm_service.snapshots_service()
        snapshots = snapshots_service.list()
        snap_active = [snap for snap in snapshots if (snap.snapshot_type == otypes.SnapshotType.ACTIVE)][0]
        snap_stateless = [snap for snap in snapshots if (snap.snapshot_type == otypes.SnapshotType.STATELESS)]
        if snap_stateless:
            wait(service=snapshots_service.snapshot_service(snap_stateless[0].id), condition=(lambda snap: (snap is None)), wait=self.param('wait'), timeout=self.param('timeout'))
        wait(service=snapshots_service.snapshot_service(snap_active.id), condition=(lambda snap: (snap.snapshot_status == otypes.SnapshotStatus.OK)), wait=self.param('wait'), timeout=self.param('timeout'))
    return True