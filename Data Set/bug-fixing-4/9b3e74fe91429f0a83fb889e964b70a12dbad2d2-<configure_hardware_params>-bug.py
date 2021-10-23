def configure_hardware_params(self, vm_obj):
    '\n        Function to configure hardware related configuration of virtual machine\n        Args:\n            vm_obj: virtual machine object\n        '
    if ('hardware' in self.params):
        if ('max_connections' in self.params['hardware']):
            self.configspec.maxMksConnections = int(self.params['hardware']['max_connections'])
            if ((vm_obj is None) or (self.configspec.maxMksConnections != vm_obj.config.hardware.maxMksConnections)):
                self.change_detected = True
        if ('nested_virt' in self.params['hardware']):
            self.configspec.nestedHVEnabled = bool(self.params['hardware']['nested_virt'])
            if ((vm_obj is None) or (self.configspec.nestedHVEnabled != bool(vm_obj.config.nestedHVEnabled))):
                self.change_detected = True
        if ('version' in self.params['hardware']):
            hw_version_check_failed = False
            temp_version = self.params['hardware'].get('version', 10)
            try:
                temp_version = int(temp_version)
            except ValueError:
                hw_version_check_failed = True
            if (temp_version not in range(3, 15)):
                hw_version_check_failed = True
            if hw_version_check_failed:
                self.module.fail_json(msg=("Failed to set hardware.version '%s' value as valid values range from 3 (ESX 2.x) to 14 (ESXi 6.5 and greater)." % temp_version))
            version = ('vmx-%02d' % temp_version)
            self.configspec.version = version
            if ((vm_obj is None) or (self.configspec.version != vm_obj.config.version)):
                self.change_detected = True
            if (vm_obj is not None):
                current_version = vm_obj.config.version
                version_digit = int(current_version.split('-', 1)[(- 1)])
                if (temp_version < version_digit):
                    self.module.fail_json(msg=("Current hardware version '%d' which is greater than the specified version '%d'. Downgrading hardware version is not supported. Please specify version greater than the current version." % (version_digit, temp_version)))
                new_version = ('vmx-%02d' % temp_version)
                try:
                    task = vm_obj.UpgradeVM_Task(new_version)
                    self.wait_for_task(task)
                    if (task.info.state != 'error'):
                        self.change_detected = True
                except vim.fault.AlreadyUpgraded:
                    pass
        if ('virt_based_security' in self.params['hardware']):
            host_version = self.select_host().summary.config.product.version
            if ((int(host_version.split('.')[0]) < 6) or ((int(host_version.split('.')[0]) == 6) and (int(host_version.split('.')[1]) < 7))):
                self.module.fail_json(msg=('ESXi version %s not support VBS.' % host_version))
            guest_ids = ['windows9_64Guest', 'windows9Server64Guest']
            if (vm_obj is None):
                guestid = self.configspec.guestId
            else:
                guestid = vm_obj.summary.config.guestId
            if (guestid not in guest_ids):
                self.module.fail_json(msg=("Guest '%s' not support VBS." % guestid))
            if (((vm_obj is None) and (int(self.configspec.version.split('-')[1]) >= 14)) or (vm_obj and (int(vm_obj.config.version.split('-')[1]) >= 14) and (vm_obj.runtime.powerState == vim.VirtualMachinePowerState.poweredOff))):
                self.configspec.flags = vim.vm.FlagInfo()
                self.configspec.flags.vbsEnabled = bool(self.params['hardware']['virt_based_security'])
                if bool(self.params['hardware']['virt_based_security']):
                    self.configspec.flags.vvtdEnabled = True
                    self.configspec.nestedHVEnabled = True
                    if (((vm_obj is None) and (self.configspec.firmware == 'efi')) or (vm_obj and (vm_obj.config.firmware == 'efi'))):
                        self.configspec.bootOptions = vim.vm.BootOptions()
                        self.configspec.bootOptions.efiSecureBootEnabled = True
                    else:
                        self.module.fail_json(msg='Not support VBS when firmware is BIOS.')
                if ((vm_obj is None) or (self.configspec.flags.vbsEnabled != vm_obj.config.flags.vbsEnabled)):
                    self.change_detected = True