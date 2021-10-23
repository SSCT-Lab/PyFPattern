def configure_resource_alloc_info(self, vm_obj):
    '\n        Function to configure resource allocation information about virtual machine\n        :param vm_obj: VM object in case of reconfigure, None in case of deploy\n        :return: None\n        '
    self.configspec.memoryAllocation = vim.ResourceAllocationInfo()
    self.configspec.cpuAllocation = vim.ResourceAllocationInfo()
    if ('hardware' in self.params):
        if ('mem_limit' in self.params['hardware']):
            mem_limit = None
            try:
                mem_limit = int(self.params['hardware'].get('mem_limit'))
            except ValueError as e:
                self.module.fail_json(msg='hardware.mem_limit attribute should be an integer value.')
            self.configspec.memoryAllocation.limit = mem_limit
            if ((vm_obj is None) or (self.configspec.memoryAllocation.limit != vm_obj.config.memoryAllocation.limit)):
                self.change_detected = True
        if ('mem_reservation' in self.params['hardware']):
            mem_reservation = None
            try:
                mem_reservation = int(self.params['hardware'].get('mem_reservation'))
            except ValueError as e:
                self.module.fail_json(msg='hardware.mem_reservation should be an integer value.')
            self.configspec.memoryAllocation.reservation = mem_reservation
            if ((vm_obj is None) or (self.configspec.memoryAllocation.reservation != vm_obj.config.memoryAllocation.reservation)):
                self.change_detected = True
        if ('cpu_limit' in self.params['hardware']):
            cpu_limit = None
            try:
                cpu_limit = int(self.params['hardware'].get('cpu_limit'))
            except ValueError as e:
                self.module.fail_json(msg='hardware.cpu_limit attribute should be an integer value.')
            self.configspec.cpuAllocation.limit = cpu_limit
            if ((vm_obj is None) or (self.configspec.cpuAllocation.limit != vm_obj.config.cpuAllocation.limit)):
                self.change_detected = True
        if ('cpu_reservation' in self.params['hardware']):
            cpu_reservation = None
            try:
                cpu_reservation = int(self.params['hardware'].get('cpu_reservation'))
            except ValueError as e:
                self.module.fail_json(msg='hardware.cpu_reservation should be an integer value.')
            self.configspec.cpuAllocation.reservation = cpu_reservation
            if ((vm_obj is None) or (self.configspec.cpuAllocation.reservation != vm_obj.config.cpuAllocation.reservation)):
                self.change_detected = True