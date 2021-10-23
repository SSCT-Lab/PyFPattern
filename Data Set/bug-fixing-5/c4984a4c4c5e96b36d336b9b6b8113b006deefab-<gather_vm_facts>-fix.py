def gather_vm_facts(content, vm):
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
        'guest_tools_status': vm.guest.toolsRunningStatus,
        'guest_tools_version': vm.guest.toolsVersion,
        'ipv4': None,
        'ipv6': None,
        'annotation': vm.config.annotation,
        'customvalues': {
            
        },
        'snapshots': [],
        'current_snapshot': None,
    }
    cfm = content.customFieldsManager
    for value_obj in vm.summary.customValue:
        kn = value_obj.key
        if ((cfm is not None) and cfm.field):
            for f in cfm.field:
                if (f.key == value_obj.key):
                    kn = f.name
                    break
        facts['customvalues'][kn] = value_obj.value
    net_dict = {
        
    }
    for device in vm.guest.net:
        net_dict[device.macAddress] = list(device.ipAddress)
    for (k, v) in iteritems(net_dict):
        for ipaddress in v:
            if ipaddress:
                if ('::' in ipaddress):
                    facts['ipv6'] = ipaddress
                else:
                    facts['ipv4'] = ipaddress
    ethernet_idx = 0
    for (idx, entry) in enumerate(vm.config.hardware.device):
        if (not hasattr(entry, 'macAddress')):
            continue
        mac_addr = mac_addr_dash = None
        if entry.macAddress:
            mac_addr_dash = entry.macAddress.replace(':', '-')
            mac_addr = entry.macAddress
        factname = ('hw_eth' + str(ethernet_idx))
        facts[factname] = {
            'addresstype': entry.addressType,
            'label': entry.deviceInfo.label,
            'macaddress': mac_addr,
            'ipaddresses': net_dict.get(entry.macAddress, None),
            'macaddress_dash': mac_addr_dash,
            'summary': entry.deviceInfo.summary,
        }
        facts['hw_interfaces'].append(('eth' + str(ethernet_idx)))
        ethernet_idx += 1
    snapshot_facts = list_snapshots(vm)
    if ('snapshots' in snapshot_facts):
        facts['snapshots'] = snapshot_facts['snapshots']
        facts['current_snapshot'] = snapshot_facts['current_snapshot']
    return facts