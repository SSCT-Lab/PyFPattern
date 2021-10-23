def get_all_virtual_machines(self):
    '\n        Function to get all virtual machines and related configurations information\n        '
    virtual_machines = get_all_objs(self.content, [vim.VirtualMachine])
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
        all_devices = _get_vm_prop(vm, ('config', 'hardware', 'device'))
        if all_devices:
            for dev in all_devices:
                if isinstance(dev, vim.vm.device.VirtualEthernetCard):
                    _mac_address.append(dev.macAddress)
        net_dict = {
            
        }
        vmnet = _get_vm_prop(vm, ('guest', 'net'))
        if vmnet:
            for device in vmnet:
                net_dict[device.macAddress] = dict()
                net_dict[device.macAddress]['ipv4'] = []
                net_dict[device.macAddress]['ipv6'] = []
                for ip_addr in device.ipAddress:
                    if ('::' in ip_addr):
                        net_dict[device.macAddress]['ipv6'].append(ip_addr)
                    else:
                        net_dict[device.macAddress]['ipv4'].append(ip_addr)
        esxi_hostname = None
        if summary.runtime.host:
            esxi_hostname = summary.runtime.host.summary.config.name
        virtual_machine = {
            summary.config.name: {
                'guest_fullname': summary.config.guestFullName,
                'power_state': summary.runtime.powerState,
                'ip_address': _ip_address,
                'mac_address': _mac_address,
                'uuid': summary.config.uuid,
                'vm_network': net_dict,
                'esxi_hostname': esxi_hostname,
            },
        }
        vm_type = self.module.params.get('vm_type')
        is_template = _get_vm_prop(vm, ('config', 'template'))
        if ((vm_type == 'vm') and (not is_template)):
            _virtual_machines.update(virtual_machine)
        elif ((vm_type == 'template') and is_template):
            _virtual_machines.update(virtual_machine)
        elif (vm_type == 'all'):
            _virtual_machines.update(virtual_machine)
    return _virtual_machines