def get_all_virtual_machines(content):
    virtual_machines = get_all_objs(content, [vim.VirtualMachine])
    _virtual_machines = {
        
    }
    for vm in virtual_machines:
        _ip_address = ''
        summary = vm.summary
        if (summary.guest is not None):
            _ip_address = summary.guest.ipAddress
            if (_ip_address is None):
                _ip_address = ''
        _mac_address = []
        if (vm.config is not None):
            for dev in vm.config.hardware.device:
                if isinstance(dev, vim.vm.device.VirtualEthernetCard):
                    _mac_address.append(dev.macAddress)
        virtual_machine = {
            summary.config.name: {
                'guest_fullname': summary.config.guestFullName,
                'power_state': summary.runtime.powerState,
                'ip_address': _ip_address,
                'mac_address': _mac_address,
                'uuid': summary.config.uuid,
            },
        }
        _virtual_machines.update(virtual_machine)
    return _virtual_machines