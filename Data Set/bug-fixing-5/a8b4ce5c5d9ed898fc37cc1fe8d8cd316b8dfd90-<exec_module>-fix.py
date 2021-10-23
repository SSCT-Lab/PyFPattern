def exec_module(self, **kwargs):
    for key in (list(self.module_arg_spec.keys()) + ['tags']):
        setattr(self, key, kwargs[key])
    self.remove_on_absent = set([resource.lower() for resource in self.remove_on_absent])
    if (not self.virtual_network_resource_group):
        self.virtual_network_resource_group = self.resource_group
    changed = False
    results = dict()
    vmss = None
    disable_ssh_password = None
    vmss_dict = None
    virtual_network = None
    subnet = None
    image_reference = None
    custom_image = False
    resource_group = self.get_resource_group(self.resource_group)
    if (not self.location):
        self.location = resource_group.location
    if (self.state == 'present'):
        if (self.vm_size and (not self.vm_size_is_valid())):
            self.fail('Parameter error: vm_size {0} is not valid for your subscription and location.'.format(self.vm_size))
        if self.ssh_public_keys:
            msg = 'Parameter error: expecting ssh_public_keys to be a list of type dict where each dict contains keys: path, key_data.'
            for key in self.ssh_public_keys:
                if (not isinstance(key, dict)):
                    self.fail(msg)
                if ((not key.get('path')) or (not key.get('key_data'))):
                    self.fail(msg)
        if (self.image and isinstance(self.image, dict)):
            if all(((key in self.image) for key in ('publisher', 'offer', 'sku', 'version'))):
                marketplace_image = self.get_marketplace_image_version()
                if (self.image['version'] == 'latest'):
                    self.image['version'] = marketplace_image.name
                    self.log('Using image version {0}'.format(self.image['version']))
                image_reference = self.compute_models.ImageReference(publisher=self.image['publisher'], offer=self.image['offer'], sku=self.image['sku'], version=self.image['version'])
            elif self.image.get('name'):
                custom_image = True
                image_reference = self.get_custom_image_reference(self.image.get('name'), self.image.get('resource_group'))
            else:
                self.fail('parameter error: expecting image to contain [publisher, offer, sku, version] or [name, resource_group]')
        elif (self.image and isinstance(self.image, str)):
            custom_image = True
            image_reference = self.get_custom_image_reference(self.image)
        elif self.image:
            self.fail('parameter error: expecting image to be a string or dict not {0}'.format(type(self.image).__name__))
        disable_ssh_password = (not self.ssh_password_enabled)
    try:
        self.log('Fetching virtual machine scale set {0}'.format(self.name))
        vmss = self.compute_client.virtual_machine_scale_sets.get(self.resource_group, self.name)
        self.check_provisioning_state(vmss, self.state)
        vmss_dict = self.serialize_vmss(vmss)
        if (self.state == 'present'):
            differences = []
            results = vmss_dict
            if (self.os_disk_caching and (self.os_disk_caching != vmss_dict['properties']['virtualMachineProfile']['storageProfile']['osDisk']['caching'])):
                self.log('CHANGED: virtual machine scale set {0} - OS disk caching'.format(self.name))
                differences.append('OS Disk caching')
                changed = True
                vmss_dict['properties']['virtualMachineProfile']['storageProfile']['osDisk']['caching'] = self.os_disk_caching
            if (self.capacity and (self.capacity != vmss_dict['sku']['capacity'])):
                self.log('CHANGED: virtual machine scale set {0} - Capacity'.format(self.name))
                differences.append('Capacity')
                changed = True
                vmss_dict['sku']['capacity'] = self.capacity
            if (self.data_disks and (len(self.data_disks) != len(vmss_dict['properties']['virtualMachineProfile']['storageProfile'].get('dataDisks', [])))):
                self.log('CHANGED: virtual machine scale set {0} - Data Disks'.format(self.name))
                differences.append('Data Disks')
                changed = True
            (update_tags, vmss_dict['tags']) = self.update_tags(vmss_dict.get('tags', dict()))
            if update_tags:
                differences.append('Tags')
                changed = True
            self.differences = differences
        elif (self.state == 'absent'):
            self.log("CHANGED: virtual machine scale set {0} exists and requested state is 'absent'".format(self.name))
            results = dict()
            changed = True
    except CloudError:
        self.log('Virtual machine scale set {0} does not exist'.format(self.name))
        if (self.state == 'present'):
            self.log("CHANGED: virtual machine scale set {0} does not exist but state is 'present'.".format(self.name))
            changed = True
    self.results['changed'] = changed
    self.results['ansible_facts']['azure_vmss'] = results
    if self.check_mode:
        return self.results
    if changed:
        if (self.state == 'present'):
            if (not vmss):
                self.log('Create virtual machine scale set {0}'.format(self.name))
                self.results['actions'].append('Created VMSS {0}'.format(self.name))
                if (not self.admin_username):
                    self.fail('Parameter error: admin_username required when creating a virtual machine scale set.')
                if (self.os_type == 'Linux'):
                    if (disable_ssh_password and (not self.ssh_public_keys)):
                        self.fail('Parameter error: ssh_public_keys required when disabling SSH password.')
                if (not self.virtual_network_name):
                    default_vnet = self.create_default_vnet()
                    virtual_network = default_vnet.id
                    self.virtual_network_name = default_vnet.name
                if self.subnet_name:
                    subnet = self.get_subnet(self.virtual_network_name, self.subnet_name)
                load_balancer_backend_address_pools = None
                load_balancer_inbound_nat_pools = None
                if self.load_balancer:
                    load_balancer = self.get_load_balancer(self.load_balancer)
                    load_balancer_backend_address_pools = ([self.compute_models.SubResource(resource.id) for resource in load_balancer.backend_address_pools] if load_balancer.backend_address_pools else None)
                    load_balancer_inbound_nat_pools = ([self.compute_models.SubResource(resource.id) for resource in load_balancer.inbound_nat_pools] if load_balancer.inbound_nat_pools else None)
                if (not self.short_hostname):
                    self.short_hostname = self.name
                if (not image_reference):
                    self.fail('Parameter error: an image is required when creating a virtual machine.')
                managed_disk = self.compute_models.VirtualMachineScaleSetManagedDiskParameters(storage_account_type=self.managed_disk_type)
                vmss_resource = self.compute_models.VirtualMachineScaleSet(self.location, tags=self.tags, upgrade_policy=self.compute_models.UpgradePolicy(mode=self.upgrade_policy), sku=self.compute_models.Sku(name=self.vm_size, capacity=self.capacity, tier=self.tier), virtual_machine_profile=self.compute_models.VirtualMachineScaleSetVMProfile(os_profile=self.compute_models.VirtualMachineScaleSetOSProfile(admin_username=self.admin_username, computer_name_prefix=self.short_hostname), storage_profile=self.compute_models.VirtualMachineScaleSetStorageProfile(os_disk=self.compute_models.VirtualMachineScaleSetOSDisk(managed_disk=managed_disk, create_option=self.compute_models.DiskCreateOptionTypes.from_image, caching=self.os_disk_caching), image_reference=image_reference), network_profile=self.compute_models.VirtualMachineScaleSetNetworkProfile(network_interface_configurations=[self.compute_models.VirtualMachineScaleSetNetworkConfiguration(name=self.name, primary=True, ip_configurations=[self.compute_models.VirtualMachineScaleSetIPConfiguration(name='default', subnet=self.compute_models.ApiEntityReference(id=subnet.id), primary=True, load_balancer_backend_address_pools=load_balancer_backend_address_pools, load_balancer_inbound_nat_pools=load_balancer_inbound_nat_pools)])])))
                if self.admin_password:
                    vmss_resource.virtual_machine_profile.os_profile.admin_password = self.admin_password
                if (self.os_type == 'Linux'):
                    vmss_resource.virtual_machine_profile.os_profile.linux_configuration = self.compute_models.LinuxConfiguration(disable_password_authentication=disable_ssh_password)
                if self.ssh_public_keys:
                    ssh_config = self.compute_models.SshConfiguration()
                    ssh_config.public_keys = [self.compute_models.SshPublicKey(path=key['path'], key_data=key['key_data']) for key in self.ssh_public_keys]
                    vmss_resource.virtual_machine_profile.os_profile.linux_configuration.ssh = ssh_config
                if self.data_disks:
                    data_disks = []
                    for data_disk in self.data_disks:
                        data_disk_managed_disk = self.compute_models.VirtualMachineScaleSetManagedDiskParameters(storage_account_type=data_disk['managed_disk_type'])
                        data_disk['caching'] = data_disk.get('caching', self.compute_models.CachingTypes.read_only)
                        data_disks.append(self.compute_models.VirtualMachineScaleSetDataDisk(lun=data_disk['lun'], caching=data_disk['caching'], create_option=self.compute_models.DiskCreateOptionTypes.empty, disk_size_gb=data_disk['disk_size_gb'], managed_disk=data_disk_managed_disk))
                    vmss_resource.virtual_machine_profile.storage_profile.data_disks = data_disks
                self.log('Create virtual machine with parameters:')
                self.create_or_update_vmss(vmss_resource)
            elif (self.differences and (len(self.differences) > 0)):
                self.log('Update virtual machine scale set {0}'.format(self.name))
                self.results['actions'].append('Updated VMSS {0}'.format(self.name))
                vmss_resource = self.get_vmss()
                vmss_resource.virtual_machine_profile.storage_profile.os_disk.caching = self.os_disk_caching
                vmss_resource.sku.capacity = self.capacity
                data_disks = []
                for data_disk in self.data_disks:
                    data_disks.append(self.compute_models.VirtualMachineScaleSetDataDisk(lun=data_disk['lun'], caching=data_disk['caching'], create_option=self.compute_models.DiskCreateOptionTypes.empty, disk_size_gb=data_disk['disk_size_gb'], managed_disk=self.compute_models.VirtualMachineScaleSetManagedDiskParameters(storage_account_type=data_disk['managed_disk_type'])))
                vmss_resource.virtual_machine_profile.storage_profile.data_disks = data_disks
                self.log('Update virtual machine with parameters:')
                self.create_or_update_vmss(vmss_resource)
            self.results['ansible_facts']['azure_vmss'] = self.serialize_vmss(self.get_vmss())
        elif (self.state == 'absent'):
            self.log('Delete virtual machine scale set {0}'.format(self.name))
            self.results['ansible_facts']['azure_vmss'] = None
            self.delete_vmss(vmss)
    del self.results['actions']
    return self.results