

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
        'hw_cores_per_socket': vm.config.hardware.numCoresPerSocket,
        'hw_memtotal_mb': vm.config.hardware.memoryMB,
        'hw_interfaces': [],
        'hw_datastores': [],
        'hw_files': [],
        'hw_esxi_host': None,
        'hw_guest_ha_state': None,
        'hw_is_template': vm.config.template,
        'hw_folder': None,
        'hw_version': vm.config.version,
        'instance_uuid': vm.config.instanceUuid,
        'guest_tools_status': _get_vm_prop(vm, ('guest', 'toolsRunningStatus')),
        'guest_tools_version': _get_vm_prop(vm, ('guest', 'toolsVersion')),
        'guest_question': vm.summary.runtime.question,
        'guest_consolidation_needed': vm.summary.runtime.consolidationNeeded,
        'ipv4': None,
        'ipv6': None,
        'annotation': vm.config.annotation,
        'customvalues': {
            
        },
        'snapshots': [],
        'current_snapshot': None,
        'vnc': {
            
        },
    }
    if vm.summary.runtime.host:
        try:
            host = vm.summary.runtime.host
            facts['hw_esxi_host'] = host.summary.config.name
        except vim.fault.NoPermission:
            pass
    if vm.summary.runtime.dasVmProtection:
        facts['hw_guest_ha_state'] = vm.summary.runtime.dasVmProtection.dasProtected
    datastores = vm.datastore
    for ds in datastores:
        facts['hw_datastores'].append(ds.info.name)
    try:
        files = vm.config.files
        layout = vm.layout
        if files:
            facts['hw_files'] = [files.vmPathName]
            for item in layout.snapshot:
                for snap in item.snapshotFile:
                    facts['hw_files'].append((files.snapshotDirectory + snap))
            for item in layout.configFile:
                facts['hw_files'].append(((os.path.dirname(files.vmPathName) + '/') + item))
            for item in vm.layout.logFile:
                facts['hw_files'].append((files.logDirectory + item))
            for item in vm.layout.disk:
                for disk in item.diskFile:
                    facts['hw_files'].append(disk)
    except Exception:
        pass
    facts['hw_folder'] = PyVmomi.get_vm_path(content, vm)
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
    vmnet = _get_vm_prop(vm, ('guest', 'net'))
    if vmnet:
        for device in vmnet:
            net_dict[device.macAddress] = list(device.ipAddress)
    if vm.guest.ipAddress:
        if (':' in vm.guest.ipAddress):
            facts['ipv6'] = vm.guest.ipAddress
        else:
            facts['ipv4'] = vm.guest.ipAddress
    ethernet_idx = 0
    for entry in vm.config.hardware.device:
        if (not hasattr(entry, 'macAddress')):
            continue
        if entry.macAddress:
            mac_addr = entry.macAddress
            mac_addr_dash = mac_addr.replace(':', '-')
        else:
            mac_addr = mac_addr_dash = None
        if (hasattr(entry, 'backing') and hasattr(entry.backing, 'port') and hasattr(entry.backing.port, 'portKey') and hasattr(entry.backing.port, 'portgroupKey')):
            port_group_key = entry.backing.port.portgroupKey
            port_key = entry.backing.port.portKey
        else:
            port_group_key = None
            port_key = None
        factname = ('hw_eth' + str(ethernet_idx))
        facts[factname] = {
            'addresstype': entry.addressType,
            'label': entry.deviceInfo.label,
            'macaddress': mac_addr,
            'ipaddresses': net_dict.get(entry.macAddress, None),
            'macaddress_dash': mac_addr_dash,
            'summary': entry.deviceInfo.summary,
            'portgroup_portkey': port_key,
            'portgroup_key': port_group_key,
        }
        facts['hw_interfaces'].append(('eth' + str(ethernet_idx)))
        ethernet_idx += 1
    snapshot_facts = list_snapshots(vm)
    if ('snapshots' in snapshot_facts):
        facts['snapshots'] = snapshot_facts['snapshots']
        facts['current_snapshot'] = snapshot_facts['current_snapshot']
    facts['vnc'] = get_vnc_extraconfig(vm)
    return facts
