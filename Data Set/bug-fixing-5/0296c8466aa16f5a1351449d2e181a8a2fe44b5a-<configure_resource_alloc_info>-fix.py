def configure_resource_alloc_info(self, vm_obj):
    '\n        Function to configure resource allocation information about virtual machine\n        :param vm_obj: VM object in case of reconfigure, None in case of deploy\n        :return: None\n        '
    rai_change_detected = False
    memory_allocation = vim.ResourceAllocationInfo()
    cpu_allocation = vim.ResourceAllocationInfo()
    if ('hardware' in self.params):
        if ('mem_limit' in self.params['hardware']):
            mem_limit = None
            try:
                mem_limit = int(self.params['hardware'].get('mem_limit'))
            except ValueError as e:
                self.module.fail_json(msg='hardware.mem_limit attribute should be an integer value.')
            memory_allocation.limit = mem_limit
            if ((vm_obj is None) or (memory_allocation.limit != vm_obj.config.memoryAllocation.limit)):
                rai_change_detected = True
        if ('mem_reservation' in self.params['hardware']):
            mem_reservation = None
            try:
                mem_reservation = int(self.params['hardware'].get('mem_reservation'))
            except ValueError as e:
                self.module.fail_json(msg='hardware.mem_reservation should be an integer value.')
            memory_allocation.reservation = mem_reservation
            if ((vm_obj is None) or (memory_allocation.reservation != vm_obj.config.memoryAllocation.reservation)):
                rai_change_detected = True
        if ('cpu_limit' in self.params['hardware']):
            cpu_limit = None
            try:
                cpu_limit = int(self.params['hardware'].get('cpu_limit'))
            except ValueError as e:
                self.module.fail_json(msg='hardware.cpu_limit attribute should be an integer value.')
            cpu_allocation.limit = cpu_limit
            if ((vm_obj is None) or (cpu_allocation.limit != vm_obj.config.cpuAllocation.limit)):
                rai_change_detected = True
        if ('cpu_reservation' in self.params['hardware']):
            cpu_reservation = None
            try:
                cpu_reservation = int(self.params['hardware'].get('cpu_reservation'))
            except ValueError as e:
                self.module.fail_json(msg='hardware.cpu_reservation should be an integer value.')
            cpu_allocation.reservation = cpu_reservation
            if ((vm_obj is None) or (cpu_allocation.reservation != vm_obj.config.cpuAllocation.reservation)):
                rai_change_detected = True
    if rai_change_detected:
        self.configspec.memoryAllocation = memory_allocation
        self.configspec.cpuAllocation = cpu_allocation
        self.change_detected = True