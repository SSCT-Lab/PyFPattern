def configure_cpu_and_memory(self, vm_obj, vm_creation=False):
    if ('hardware' in self.params):
        if ('num_cpus' in self.params['hardware']):
            try:
                num_cpus = int(self.params['hardware']['num_cpus'])
            except ValueError:
                self.module.fail_json(msg='hardware.num_cpus attribute should be an integer value.')
            if (vm_obj and (vm_obj.runtime.powerState == vim.VirtualMachinePowerState.poweredOn)):
                if ((not vm_obj.config.cpuHotRemoveEnabled) and (num_cpus < vm_obj.config.hardware.numCPU)):
                    self.module.fail_json(msg='Configured cpu number is less than the cpu number of the VM, cpuHotRemove is not enabled')
                if ((not vm_obj.config.cpuHotAddEnabled) and (num_cpus > vm_obj.config.hardware.numCPU)):
                    self.module.fail_json(msg='Configured cpu number is more than the cpu number of the VM, cpuHotAdd is not enabled')
            if ('num_cpu_cores_per_socket' in self.params['hardware']):
                try:
                    num_cpu_cores_per_socket = int(self.params['hardware']['num_cpu_cores_per_socket'])
                except ValueError:
                    self.module.fail_json(msg='hardware.num_cpu_cores_per_socket attribute should be an integer value.')
                if ((num_cpus % num_cpu_cores_per_socket) != 0):
                    self.module.fail_json(msg='hardware.num_cpus attribute should be a multiple of hardware.num_cpu_cores_per_socket')
                self.configspec.numCoresPerSocket = num_cpu_cores_per_socket
                if ((vm_obj is None) or (self.configspec.numCoresPerSocket != vm_obj.config.hardware.numCoresPerSocket)):
                    self.change_detected = True
            self.configspec.numCPUs = num_cpus
            if ((vm_obj is None) or (self.configspec.numCPUs != vm_obj.config.hardware.numCPU)):
                self.change_detected = True
        elif (vm_creation and (not self.params['template'])):
            self.module.fail_json(msg='hardware.num_cpus attribute is mandatory for VM creation')
        if ('memory_mb' in self.params['hardware']):
            try:
                memory_mb = int(self.params['hardware']['memory_mb'])
            except ValueError:
                self.module.fail_json(msg='Failed to parse hardware.memory_mb value. Please refer the documentation and provide correct value.')
            if (vm_obj and (vm_obj.runtime.powerState == vim.VirtualMachinePowerState.poweredOn)):
                if (vm_obj.config.memoryHotAddEnabled and (memory_mb < vm_obj.config.hardware.memoryMB)):
                    self.module.fail_json(msg='Configured memory is less than memory size of the VM, operation is not supported')
                elif ((not vm_obj.config.memoryHotAddEnabled) and (memory_mb != vm_obj.config.hardware.memoryMB)):
                    self.module.fail_json(msg='memoryHotAdd is not enabled')
            self.configspec.memoryMB = memory_mb
            if ((vm_obj is None) or (self.configspec.memoryMB != vm_obj.config.hardware.memoryMB)):
                self.change_detected = True
        elif (vm_creation and (not self.params['template'])):
            self.module.fail_json(msg='hardware.memory_mb attribute is mandatory for VM creation')
        if ('hotadd_memory' in self.params['hardware']):
            if (vm_obj and (vm_obj.runtime.powerState == vim.VirtualMachinePowerState.poweredOn) and (vm_obj.config.memoryHotAddEnabled != bool(self.params['hardware']['hotadd_memory']))):
                self.module.fail_json(msg='Configure hotadd memory operation is not supported when VM is power on')
            self.configspec.memoryHotAddEnabled = bool(self.params['hardware']['hotadd_memory'])
            if ((vm_obj is None) or (self.configspec.memoryHotAddEnabled != vm_obj.config.memoryHotAddEnabled)):
                self.change_detected = True
        if ('hotadd_cpu' in self.params['hardware']):
            if (vm_obj and (vm_obj.runtime.powerState == vim.VirtualMachinePowerState.poweredOn) and (vm_obj.config.cpuHotAddEnabled != bool(self.params['hardware']['hotadd_cpu']))):
                self.module.fail_json(msg='Configure hotadd cpu operation is not supported when VM is power on')
            self.configspec.cpuHotAddEnabled = bool(self.params['hardware']['hotadd_cpu'])
            if ((vm_obj is None) or (self.configspec.cpuHotAddEnabled != vm_obj.config.cpuHotAddEnabled)):
                self.change_detected = True
        if ('hotremove_cpu' in self.params['hardware']):
            if (vm_obj and (vm_obj.runtime.powerState == vim.VirtualMachinePowerState.poweredOn) and (vm_obj.config.cpuHotRemoveEnabled != bool(self.params['hardware']['hotremove_cpu']))):
                self.module.fail_json(msg='Configure hotremove cpu operation is not supported when VM is power on')
            self.configspec.cpuHotRemoveEnabled = bool(self.params['hardware']['hotremove_cpu'])
            if ((vm_obj is None) or (self.configspec.cpuHotRemoveEnabled != vm_obj.config.cpuHotRemoveEnabled)):
                self.change_detected = True
        if ('memory_reservation' in self.params['hardware']):
            memory_reservation_mb = 0
            try:
                memory_reservation_mb = int(self.params['hardware']['memory_reservation'])
            except ValueError as e:
                self.module.fail_json(msg=('Failed to set memory_reservation value.Valid value for memory_reservation value in MB (integer): %s' % e))
            mem_alloc = vim.ResourceAllocationInfo()
            mem_alloc.reservation = memory_reservation_mb
            self.configspec.memoryAllocation = mem_alloc
            if ((vm_obj is None) or (self.configspec.memoryAllocation.reservation != vm_obj.config.memoryAllocation.reservation)):
                self.change_detected = True
        if ('memory_reservation_lock' in self.params['hardware']):
            self.configspec.memoryReservationLockedToMax = bool(self.params['hardware']['memory_reservation_lock'])
            if ((vm_obj is None) or (self.configspec.memoryReservationLockedToMax != vm_obj.config.memoryReservationLockedToMax)):
                self.change_detected = True
        if ('boot_firmware' in self.params['hardware']):
            if (vm_obj is not None):
                return
            boot_firmware = self.params['hardware']['boot_firmware'].lower()
            if (boot_firmware not in ('bios', 'efi')):
                self.module.fail_json(msg=("hardware.boot_firmware value is invalid [%s]. Need one of ['bios', 'efi']." % boot_firmware))
            self.configspec.firmware = boot_firmware
            self.change_detected = True