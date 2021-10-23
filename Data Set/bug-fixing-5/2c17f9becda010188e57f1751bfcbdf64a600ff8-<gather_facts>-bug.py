def gather_facts(self, vm):
    ' Gather facts from vim.VirtualMachine object. '
    facts = {
        'module_hw': True,
        'hw_name': vm.config.name,
        'hw_power_status': vm.summary.runtime.powerState,
        'hw_guest_full_name': vm.summary.guest.guestFullName,
        'hw_guest_id': vm.summary.guest.guestId,
        'hw_product_uuid': vm.config.uuid,
        'hw_processor_count': vm.config.hardware.numCPU,
        'hw_memtotal_mb': vm.config.hardware.memoryMB,
        'hw_interfaces': [],
        'ipv4': None,
        'ipv6': None,
    }
    netDict = {
        
    }
    for device in vm.guest.net:
        mac = device.macAddress
        ips = list(device.ipAddress)
        netDict[mac] = ips
    for (k, v) in netDict.items():
        for ipaddress in v:
            if ipaddress:
                if ('::' in ipaddress):
                    facts['ipv6'] = ipaddress
                else:
                    facts['ipv4'] = ipaddress
    for (idx, entry) in enumerate(vm.config.hardware.device):
        if (not hasattr(entry, 'macAddress')):
            continue
        factname = ('hw_eth' + str(idx))
        facts[factname] = {
            'addresstype': entry.addressType,
            'label': entry.deviceInfo.label,
            'macaddress': entry.macAddress,
            'ipaddresses': netDict.get(entry.macAddress, None),
            'macaddress_dash': entry.macAddress.replace(':', '-'),
            'summary': entry.deviceInfo.summary,
        }
        facts['hw_interfaces'].append(('eth' + str(idx)))
    return facts