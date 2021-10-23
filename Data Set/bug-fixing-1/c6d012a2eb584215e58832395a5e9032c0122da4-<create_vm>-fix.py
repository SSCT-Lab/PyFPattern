

def create_vm(vsphere_client, module, esxi, resource_pool, cluster_name, guest, vm_extra_config, vm_hardware, vm_disk, vm_nic, vm_hw_version, state):
    datacenter = esxi['datacenter']
    esxi_hostname = esxi['hostname']
    dclist = [k for (k, v) in vsphere_client.get_datacenters().items() if (v == datacenter)]
    if dclist:
        dcmor = dclist[0]
    else:
        vsphere_client.disconnect()
        module.fail_json(msg=('Cannot find datacenter named: %s' % datacenter))
    dcprops = VIProperty(vsphere_client, dcmor)
    hfmor = dcprops.hostFolder._obj
    if vm_extra_config.get('folder'):
        vmfmor = _get_folderid_for_path(vsphere_client, dcmor, vm_extra_config.get('folder'))
        if (vmfmor is None):
            for (mor, name) in vsphere_client._get_managed_objects(MORTypes.Folder).items():
                if (name == vm_extra_config['folder']):
                    vmfmor = mor
        if (vmfmor is None):
            vsphere_client.disconnect()
            module.fail_json(msg=('Cannot find folder named: %s' % vm_extra_config['folder']))
    else:
        vmfmor = dcprops.vmFolder._obj
    nfmor = dcprops.networkFolder._obj
    crmors = vsphere_client._retrieve_properties_traversal(property_names=['name', 'host'], from_node=hfmor, obj_type='ComputeResource')
    try:
        hostmor = [k for (k, v) in vsphere_client.get_hosts().items() if (v == esxi_hostname)][0]
    except IndexError:
        vsphere_client.disconnect()
        module.fail_json(msg=('Cannot find esx host named: %s' % esxi_hostname))
    crmor = None
    for cr in crmors:
        if crmor:
            break
        for p in cr.PropSet:
            if (p.Name == 'host'):
                for h in p.Val.get_element_ManagedObjectReference():
                    if (h == hostmor):
                        crmor = cr.Obj
                        break
                if crmor:
                    break
    crprops = VIProperty(vsphere_client, crmor)
    if resource_pool:
        try:
            cluster = ([k for (k, v) in vsphere_client.get_clusters().items() if (v == cluster_name)][0] if cluster_name else None)
        except IndexError:
            vsphere_client.disconnect()
            module.fail_json(msg=('Cannot find Cluster named: %s' % cluster_name))
        try:
            rpmor = [k for (k, v) in vsphere_client.get_resource_pools(from_mor=cluster).items() if (v == resource_pool)][0]
        except IndexError:
            vsphere_client.disconnect()
            module.fail_json(msg=('Cannot find Resource Pool named: %s' % resource_pool))
    else:
        rpmor = crprops.resourcePool._obj
    request = VI.QueryConfigTargetRequestMsg()
    _this = request.new__this(crprops.environmentBrowser._obj)
    _this.set_attribute_type(crprops.environmentBrowser._obj.get_attribute_type())
    request.set_element__this(_this)
    h = request.new_host(hostmor)
    h.set_attribute_type(hostmor.get_attribute_type())
    request.set_element_host(h)
    config_target = vsphere_client._proxy.QueryConfigTarget(request)._returnval
    request = VI.QueryConfigOptionRequestMsg()
    _this = request.new__this(crprops.environmentBrowser._obj)
    _this.set_attribute_type(crprops.environmentBrowser._obj.get_attribute_type())
    request.set_element__this(_this)
    h = request.new_host(hostmor)
    h.set_attribute_type(hostmor.get_attribute_type())
    request.set_element_host(h)
    config_option = vsphere_client._proxy.QueryConfigOption(request)._returnval
    default_devs = config_option.DefaultDevice
    create_vm_request = VI.CreateVM_TaskRequestMsg()
    config = create_vm_request.new_config()
    if vm_hw_version:
        config.set_element_version(vm_hw_version)
    vmfiles = config.new_files()
    (datastore_name, ds) = find_datastore(module, vsphere_client, vm_disk['disk1']['datastore'], config_target)
    vmfiles.set_element_vmPathName(datastore_name)
    config.set_element_files(vmfiles)
    config.set_element_name(guest)
    if ('notes' in vm_extra_config):
        config.set_element_annotation(vm_extra_config['notes'])
    config.set_element_memoryMB(int(vm_hardware['memory_mb']))
    config.set_element_numCPUs(int(vm_hardware['num_cpus']))
    config.set_element_guestId(vm_hardware['osid'])
    devices = []
    disk_ctrl_key = add_scsi_controller(module, vsphere_client, config, devices, vm_hardware['scsi'])
    if vm_disk:
        disk_num = 0
        disk_key = 0
        bus_num = 0
        disk_ctrl = 1
        for disk in sorted(vm_disk):
            try:
                datastore = vm_disk[disk]['datastore']
            except KeyError:
                vsphere_client.disconnect()
                module.fail_json(msg=('Error on %s definition. datastore needs to be specified.' % disk))
            try:
                disksize = int(vm_disk[disk]['size_gb'])
                disksize = ((disksize * 1024) * 1024)
            except (KeyError, ValueError):
                vsphere_client.disconnect()
                module.fail_json(msg=('Error on %s definition. size needs to be specified as an integer.' % disk))
            try:
                disktype = vm_disk[disk]['type']
            except KeyError:
                vsphere_client.disconnect()
                module.fail_json(msg=('Error on %s definition. type needs to be specified.' % disk))
            if (disk_num == 7):
                disk_num = (disk_num + 1)
                disk_key = (disk_key + 1)
            elif (disk_num > 15):
                bus_num = (bus_num + 1)
                disk_ctrl = (disk_ctrl + 1)
                disk_ctrl_key = add_scsi_controller(module, vsphere_client, config, devices, type=vm_hardware['scsi'], bus_num=bus_num, disk_ctrl_key=disk_ctrl)
                disk_num = 0
                disk_key = 0
            add_disk(module, vsphere_client, config_target, config, devices, datastore, disktype, disksize, disk_ctrl_key, disk_num, disk_key)
            disk_num = (disk_num + 1)
            disk_key = (disk_key + 1)
    if ('vm_cdrom' in vm_hardware):
        (cdrom_type, cdrom_iso_path) = get_cdrom_params(module, vsphere_client, vm_hardware['vm_cdrom'])
        add_cdrom(module, vsphere_client, config_target, config, devices, default_devs, cdrom_type, cdrom_iso_path)
    if ('vm_floppy' in vm_hardware):
        floppy_image_path = None
        floppy_type = None
        try:
            floppy_type = vm_hardware['vm_floppy']['type']
        except KeyError:
            vsphere_client.disconnect()
            module.fail_json(msg=('Error on %s definition. floppy type needs to be specified.' % vm_hardware['vm_floppy']))
        if (floppy_type == 'image'):
            try:
                floppy_image_path = vm_hardware['vm_floppy']['image_path']
            except KeyError:
                vsphere_client.disconnect()
                module.fail_json(msg=('Error on %s definition. floppy image_path needs to be specified.' % vm_hardware['vm_floppy']))
        add_floppy(module, vsphere_client, config_target, config, devices, default_devs, floppy_type, floppy_image_path)
    if vm_nic:
        for nic in sorted(vm_nic):
            try:
                nictype = vm_nic[nic]['type']
            except KeyError:
                vsphere_client.disconnect()
                module.fail_json(msg=('Error on %s definition. type needs to be  specified.' % nic))
            try:
                network = vm_nic[nic]['network']
            except KeyError:
                vsphere_client.disconnect()
                module.fail_json(msg=('Error on %s definition. network needs to be  specified.' % nic))
            try:
                network_type = vm_nic[nic]['network_type']
            except KeyError:
                vsphere_client.disconnect()
                module.fail_json(msg=('Error on %s definition. network_type needs to be  specified.' % nic))
            add_nic(module, vsphere_client, nfmor, config, devices, nictype, network, network_type)
    config.set_element_deviceChange(devices)
    create_vm_request.set_element_config(config)
    folder_mor = create_vm_request.new__this(vmfmor)
    folder_mor.set_attribute_type(vmfmor.get_attribute_type())
    create_vm_request.set_element__this(folder_mor)
    rp_mor = create_vm_request.new_pool(rpmor)
    rp_mor.set_attribute_type(rpmor.get_attribute_type())
    create_vm_request.set_element_pool(rp_mor)
    host_mor = create_vm_request.new_host(hostmor)
    host_mor.set_attribute_type(hostmor.get_attribute_type())
    create_vm_request.set_element_host(host_mor)
    taskmor = vsphere_client._proxy.CreateVM_Task(create_vm_request)._returnval
    task = VITask(taskmor, vsphere_client)
    task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
    if (task.get_state() == task.STATE_ERROR):
        vsphere_client.disconnect()
        module.fail_json(msg=('Error creating vm: %s' % task.get_error_message()))
    else:
        vm = vsphere_client.get_vm_by_name(guest)
        if vm_extra_config:
            vm.set_extra_config(vm_extra_config)
        power_state(vm, state, True)
        vmfacts = gather_facts(vm)
        vsphere_client.disconnect()
        module.exit_json(ansible_facts=vmfacts, changed=True, changes=('Created VM %s' % guest))
