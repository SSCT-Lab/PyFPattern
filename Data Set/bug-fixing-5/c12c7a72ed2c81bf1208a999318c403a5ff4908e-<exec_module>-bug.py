def exec_module(self, **kwargs):
    for key in (list(self.module_arg_spec.keys()) + ['tags']):
        setattr(self, key, kwargs[key])
    self.remove_on_absent = set([resource.lower() for resource in self.remove_on_absent])
    changed = False
    powerstate_change = None
    results = dict()
    vm = None
    network_interfaces = []
    requested_vhd_uri = None
    data_disk_requested_vhd_uri = None
    disable_ssh_password = None
    vm_dict = None
    resource_group = self.get_resource_group(self.resource_group)
    if (not self.location):
        self.location = resource_group.location
    if (self.state == 'present'):
        if (self.vm_size and (not self.vm_size_is_valid())):
            self.fail('Parameter error: vm_size {0} is not valid for your subscription and location.'.format(self.vm_size))
        if self.network_interface_names:
            for name in self.network_interface_names:
                nic = self.get_network_interface(name)
                network_interfaces.append(nic.id)
        if self.ssh_public_keys:
            msg = 'Parameter error: expecting ssh_public_keys to be a list of type dict where each dict contains keys: path, key_data.'
            for key in self.ssh_public_keys:
                if (not isinstance(key, dict)):
                    self.fail(msg)
                if ((not key.get('path')) or (not key.get('key_data'))):
                    self.fail(msg)
        if self.image:
            if ((not self.image.get('publisher')) or (not self.image.get('offer')) or (not self.image.get('sku')) or (not self.image.get('version'))):
                self.error('parameter error: expecting image to contain publisher, offer, sku and version keys.')
            image_version = self.get_image_version()
            if (self.image['version'] == 'latest'):
                self.image['version'] = image_version.name
                self.log('Using image version {0}'.format(self.image['version']))
        if ((not self.storage_blob_name) and (not self.managed_disk_type)):
            self.storage_blob_name = (self.name + '.vhd')
        elif self.managed_disk_type:
            self.storage_blob_name = self.name
        if (self.storage_account_name and (not self.managed_disk_type)):
            self.get_storage_account(self.storage_account_name)
            requested_vhd_uri = 'https://{0}.blob.{1}/{2}/{3}'.format(self.storage_account_name, self._cloud_environment.suffixes.storage_endpoint, self.storage_container_name, self.storage_blob_name)
        disable_ssh_password = (not self.ssh_password_enabled)
    try:
        self.log('Fetching virtual machine {0}'.format(self.name))
        vm = self.compute_client.virtual_machines.get(self.resource_group, self.name, expand='instanceview')
        self.check_provisioning_state(vm, self.state)
        vm_dict = self.serialize_vm(vm)
        if (self.state == 'present'):
            differences = []
            current_nics = []
            results = vm_dict
            if self.network_interface_names:
                for nic in vm_dict['properties']['networkProfile']['networkInterfaces']:
                    current_nics.append(nic['id'])
                if (set(current_nics) != set(network_interfaces)):
                    self.log('CHANGED: virtual machine {0} - network interfaces are different.'.format(self.name))
                    differences.append('Network Interfaces')
                    updated_nics = [dict(id=id) for id in network_interfaces]
                    vm_dict['properties']['networkProfile']['networkInterfaces'] = updated_nics
                    changed = True
            if (self.os_disk_caching and (self.os_disk_caching != vm_dict['properties']['storageProfile']['osDisk']['caching'])):
                self.log('CHANGED: virtual machine {0} - OS disk caching'.format(self.name))
                differences.append('OS Disk caching')
                changed = True
                vm_dict['properties']['storageProfile']['osDisk']['caching'] = self.os_disk_caching
            (update_tags, vm_dict['tags']) = self.update_tags(vm_dict.get('tags', dict()))
            if update_tags:
                differences.append('Tags')
                changed = True
            if (self.short_hostname and (self.short_hostname != vm_dict['properties']['osProfile']['computerName'])):
                self.log('CHANGED: virtual machine {0} - short hostname'.format(self.name))
                differences.append('Short Hostname')
                changed = True
                vm_dict['properties']['osProfile']['computerName'] = self.short_hostname
            if (self.started and (vm_dict['powerstate'] != 'running')):
                self.log("CHANGED: virtual machine {0} not running and requested state 'running'".format(self.name))
                changed = True
                powerstate_change = 'poweron'
            elif ((self.state == 'present') and (vm_dict['powerstate'] == 'running') and self.restarted):
                self.log("CHANGED: virtual machine {0} {1} and requested state 'restarted'".format(self.name, vm_dict['powerstate']))
                changed = True
                powerstate_change = 'restarted'
            elif ((self.state == 'present') and (not self.allocated) and (vm_dict['powerstate'] != 'deallocated')):
                self.log("CHANGED: virtual machine {0} {1} and requested state 'deallocated'".format(self.name, vm_dict['powerstate']))
                changed = True
                powerstate_change = 'deallocated'
            elif ((not self.started) and (vm_dict['powerstate'] == 'running')):
                self.log("CHANGED: virtual machine {0} running and requested state 'stopped'".format(self.name))
                changed = True
                powerstate_change = 'poweroff'
            self.differences = differences
        elif (self.state == 'absent'):
            self.log("CHANGED: virtual machine {0} exists and requested state is 'absent'".format(self.name))
            results = dict()
            changed = True
    except CloudError:
        self.log('Virtual machine {0} does not exist'.format(self.name))
        if (self.state == 'present'):
            self.log("CHANGED: virtual machine {0} does not exist but state is 'present'.".format(self.name))
            changed = True
    self.results['changed'] = changed
    self.results['ansible_facts']['azure_vm'] = results
    self.results['powerstate_change'] = powerstate_change
    if self.check_mode:
        return self.results
    if changed:
        if (self.state == 'present'):
            if (not vm):
                self.log('Create virtual machine {0}'.format(self.name))
                self.results['actions'].append('Created VM {0}'.format(self.name))
                if (not self.admin_username):
                    self.fail('Parameter error: admin_username required when creating a virtual machine.')
                if (self.os_type == 'Linux'):
                    if (disable_ssh_password and (not self.ssh_public_keys)):
                        self.fail('Parameter error: ssh_public_keys required when disabling SSH password.')
                if (not self.image):
                    self.fail('Parameter error: an image is required when creating a virtual machine.')
                if (not self.network_interface_names):
                    default_nic = self.create_default_nic()
                    self.log('network interface:')
                    self.log(self.serialize_obj(default_nic, 'NetworkInterface'), pretty_print=True)
                    network_interfaces = [default_nic.id]
                if ((not self.storage_account_name) and (not self.managed_disk_type)):
                    storage_account = self.create_default_storage_account()
                    self.log('storage account:')
                    self.log(self.serialize_obj(storage_account, 'StorageAccount'), pretty_print=True)
                    requested_vhd_uri = 'https://{0}.blob.{1}/{2}/{3}'.format(storage_account.name, self._cloud_environment.suffixes.storage_endpoint, self.storage_container_name, self.storage_blob_name)
                if (not self.short_hostname):
                    self.short_hostname = self.name
                nics = [NetworkInterfaceReference(id=id) for id in network_interfaces]
                if (not self.managed_disk_type):
                    managed_disk = None
                    vhd = VirtualHardDisk(uri=requested_vhd_uri)
                else:
                    vhd = None
                    managed_disk = ManagedDiskParameters(storage_account_type=self.managed_disk_type)
                vm_resource = VirtualMachine(self.location, tags=self.tags, os_profile=OSProfile(admin_username=self.admin_username, computer_name=self.short_hostname), hardware_profile=HardwareProfile(vm_size=self.vm_size), storage_profile=StorageProfile(os_disk=OSDisk(name=self.storage_blob_name, vhd=vhd, managed_disk=managed_disk, create_option=DiskCreateOptionTypes.from_image, caching=self.os_disk_caching), image_reference=ImageReference(publisher=self.image['publisher'], offer=self.image['offer'], sku=self.image['sku'], version=self.image['version'])), network_profile=NetworkProfile(network_interfaces=nics))
                if self.admin_password:
                    vm_resource.os_profile.admin_password = self.admin_password
                if (self.os_type == 'Linux'):
                    vm_resource.os_profile.linux_configuration = LinuxConfiguration(disable_password_authentication=disable_ssh_password)
                if self.ssh_public_keys:
                    ssh_config = SshConfiguration()
                    ssh_config.public_keys = [SshPublicKey(path=key['path'], key_data=key['key_data']) for key in self.ssh_public_keys]
                    vm_resource.os_profile.linux_configuration.ssh = ssh_config
                if self.data_disks:
                    data_disks = []
                    count = 0
                    for data_disk in self.data_disks:
                        if (not data_disk.get('managed_disk_type')):
                            if (not data_disk.get('storage_blob_name')):
                                data_disk['storage_blob_name'] = (((self.name + '-data-') + str(count)) + '.vhd')
                                count += 1
                            if data_disk.get('storage_account_name'):
                                self.get_storage_account(data_disk['storage_account_name'])
                                data_disk_storage_account.name = data_disk['storage_account_name']
                            else:
                                data_disk_storage_account = self.create_default_storage_account()
                                self.log('data disk storage account:')
                                self.log(self.serialize_obj(data_disk_storage_account, 'StorageAccount'), pretty_print=True)
                            if (not data_disk.get('storage_container_name')):
                                data_disk['storage_container_name'] = 'vhds'
                            data_disk_requested_vhd_uri = 'https://{0}.blob.core.windows.net/{1}/{2}'.format(data_disk_storage_account.name, data_disk['storage_container_name'], data_disk['storage_blob_name'])
                        if (not data_disk.get('managed_disk_type')):
                            data_disk_managed_disk = None
                            disk_name = data_disk['storage_blob_name']
                            data_disk_vhd = VirtualHardDisk(uri=data_disk_requested_vhd_uri)
                        else:
                            data_disk_vhd = None
                            data_disk_managed_disk = ManagedDiskParameters(storage_account_type=data_disk['managed_disk_type'])
                            disk_name = ((self.name + '-datadisk-') + str(count))
                            count += 1
                        data_disk['caching'] = data_disk.get('caching', 'ReadOnly')
                        data_disks.append(DataDisk(lun=data_disk['lun'], name=disk_name, vhd=data_disk_vhd, caching=data_disk['caching'], create_option=DiskCreateOptionTypes.empty, disk_size_gb=data_disk['disk_size_gb'], managed_disk=data_disk_managed_disk))
                    vm_resource.storage_profile.data_disks = data_disks
                self.log('Create virtual machine with parameters:')
                self.create_or_update_vm(vm_resource)
            elif (self.differences and (len(self.differences) > 0)):
                self.log('Update virtual machine {0}'.format(self.name))
                self.results['actions'].append('Updated VM {0}'.format(self.name))
                nics = [NetworkInterfaceReference(id=interface['id']) for interface in vm_dict['properties']['networkProfile']['networkInterfaces']]
                if (not vm_dict['properties']['storageProfile']['osDisk'].get('managedDisk')):
                    managed_disk = None
                    vhd = VirtualHardDisk(uri=vm_dict['properties']['storageProfile']['osDisk']['vhd']['uri'])
                else:
                    vhd = None
                    managed_disk = ManagedDiskParameters(storage_account_type=vm_dict['properties']['storageProfile']['osDisk']['managedDisk']['storageAccountType'])
                vm_resource = VirtualMachine(vm_dict['location'], os_profile=OSProfile(admin_username=vm_dict['properties']['osProfile']['adminUsername'], computer_name=vm_dict['properties']['osProfile']['computerName']), hardware_profile=HardwareProfile(vm_size=vm_dict['properties']['hardwareProfile']['vmSize']), storage_profile=StorageProfile(os_disk=OSDisk(name=vm_dict['properties']['storageProfile']['osDisk']['name'], vhd=vhd, managed_disk=managed_disk, create_option=vm_dict['properties']['storageProfile']['osDisk']['createOption'], os_type=vm_dict['properties']['storageProfile']['osDisk']['osType'], caching=vm_dict['properties']['storageProfile']['osDisk']['caching']), image_reference=ImageReference(publisher=vm_dict['properties']['storageProfile']['imageReference']['publisher'], offer=vm_dict['properties']['storageProfile']['imageReference']['offer'], sku=vm_dict['properties']['storageProfile']['imageReference']['sku'], version=vm_dict['properties']['storageProfile']['imageReference']['version'])), network_profile=NetworkProfile(network_interfaces=nics))
                if vm_dict.get('tags'):
                    vm_resource.tags = vm_dict['tags']
                if vm_dict['properties']['osProfile'].get('adminPassword'):
                    vm_resource.os_profile.admin_password = vm_dict['properties']['osProfile']['adminPassword']
                linux_config = vm_dict['properties']['osProfile'].get('linuxConfiguration')
                if linux_config:
                    ssh_config = linux_config.get('ssh', None)
                    vm_resource.os_profile.linux_configuration = LinuxConfiguration(disable_password_authentication=linux_config.get('disablePasswordAuthentication', False))
                    if ssh_config:
                        public_keys = ssh_config.get('publicKeys')
                        if public_keys:
                            vm_resource.os_profile.linux_configuration.ssh = SshConfiguration(public_keys=[])
                            for key in public_keys:
                                vm_resource.os_profile.linux_configuration.ssh.public_keys.append(SshPublicKey(path=key['path'], key_data=key['keyData']))
                if vm_dict['properties']['storageProfile'].get('dataDisks'):
                    data_disks = []
                    for data_disk in vm_dict['properties']['storageProfile']['dataDisks']:
                        if data_disk.get('managedDisk'):
                            managed_disk_type = data_disk['managedDisk']['storageAccountType']
                            data_disk_managed_disk = ManagedDiskParameters(storage_account_type=managed_disk_type)
                            data_disk_vhd = None
                        else:
                            data_disk_vhd = data_disk['vhd']['uri']
                            data_disk_managed_disk = None
                        data_disks.append(DataDisk(lun=int(data_disk['lun']), name=data_disk.get('name'), vhd=data_disk_vhd, caching=data_disk.get('caching'), create_option=data_disk.get('createOption'), disk_size_gb=int(data_disk['diskSizeGB']), managed_disk=data_disk_managed_disk))
                    vm_resource.storage_profile.data_disks = data_disks
                self.log('Update virtual machine with parameters:')
                self.create_or_update_vm(vm_resource)
            if ((powerstate_change == 'poweron') and (self.results['ansible_facts']['azure_vm']['powerstate'] != 'running')):
                self.power_on_vm()
            elif ((powerstate_change == 'poweroff') and (self.results['ansible_facts']['azure_vm']['powerstate'] == 'running')):
                self.power_off_vm()
            elif (powerstate_change == 'restarted'):
                self.restart_vm()
            elif (powerstate_change == 'deallocated'):
                self.deallocate_vm()
            self.results['ansible_facts']['azure_vm'] = self.serialize_vm(self.get_vm())
        elif (self.state == 'absent'):
            self.log('Delete virtual machine {0}'.format(self.name))
            self.results['ansible_facts']['azure_vm'] = None
            self.delete_vm(vm)
    del self.results['actions']
    return self.results