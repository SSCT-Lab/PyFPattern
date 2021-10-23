def exec_module(self, **kwargs):
    for key in (list(self.module_arg_spec.keys()) + ['tags']):
        setattr(self, key, kwargs[key])
    self.remove_on_absent = set([resource.lower() for resource in self.remove_on_absent])
    self.zones = ([int(i) for i in self.zones] if self.zones else None)
    changed = False
    powerstate_change = None
    results = dict()
    vm = None
    network_interfaces = []
    requested_vhd_uri = None
    data_disk_requested_vhd_uri = None
    disable_ssh_password = None
    vm_dict = None
    image_reference = None
    custom_image = False
    resource_group = self.get_resource_group(self.resource_group)
    if (not self.location):
        self.location = resource_group.location
    self.location = normalize_location_name(self.location)
    if (self.state == 'present'):
        if (self.vm_size and (not self.vm_size_is_valid())):
            self.fail('Parameter error: vm_size {0} is not valid for your subscription and location.'.format(self.vm_size))
        if self.network_interface_names:
            for nic_name in self.network_interface_names:
                nic = self.parse_network_interface(nic_name)
                network_interfaces.append(nic)
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
        if self.plan:
            if ((not self.plan.get('name')) or (not self.plan.get('product')) or (not self.plan.get('publisher'))):
                self.fail('parameter error: plan must include name, product, and publisher')
        if ((not self.storage_blob_name) and (not self.managed_disk_type)):
            self.storage_blob_name = (self.name + '.vhd')
        elif self.managed_disk_type:
            self.storage_blob_name = self.name
        if (self.storage_account_name and (not self.managed_disk_type)):
            properties = self.get_storage_account(self.storage_account_name)
            requested_vhd_uri = '{0}{1}/{2}'.format(properties.primary_endpoints.blob, self.storage_container_name, self.storage_blob_name)
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
                    updated_nics = [dict(id=id, primary=(i == 0)) for (i, id) in enumerate(network_interfaces)]
                    vm_dict['properties']['networkProfile']['networkInterfaces'] = updated_nics
                    changed = True
            if (self.os_disk_caching and (self.os_disk_caching != vm_dict['properties']['storageProfile']['osDisk']['caching'])):
                self.log('CHANGED: virtual machine {0} - OS disk caching'.format(self.name))
                differences.append('OS Disk caching')
                changed = True
                vm_dict['properties']['storageProfile']['osDisk']['caching'] = self.os_disk_caching
            if (self.os_disk_name and (self.os_disk_name != vm_dict['properties']['storageProfile']['osDisk']['name'])):
                self.log('CHANGED: virtual machine {0} - OS disk name'.format(self.name))
                differences.append('OS Disk name')
                changed = True
                vm_dict['properties']['storageProfile']['osDisk']['name'] = self.os_disk_name
            if (self.os_disk_size_gb and (self.os_disk_size_gb != vm_dict['properties']['storageProfile']['osDisk'].get('diskSizeGB'))):
                self.log('CHANGED: virtual machine {0} - OS disk size '.format(self.name))
                differences.append('OS Disk size')
                changed = True
                vm_dict['properties']['storageProfile']['osDisk']['diskSizeGB'] = self.os_disk_size_gb
            if (self.vm_size and (self.vm_size != vm_dict['properties']['hardwareProfile']['vmSize'])):
                self.log('CHANGED: virtual machine {0} - size '.format(self.name))
                differences.append('VM size')
                changed = True
                vm_dict['properties']['hardwareProfile']['vmSize'] = self.vm_size
            (update_tags, vm_dict['tags']) = self.update_tags(vm_dict.get('tags', dict()))
            if update_tags:
                differences.append('Tags')
                changed = True
            if (self.short_hostname and (self.short_hostname != vm_dict['properties']['osProfile']['computerName'])):
                self.log('CHANGED: virtual machine {0} - short hostname'.format(self.name))
                differences.append('Short Hostname')
                changed = True
                vm_dict['properties']['osProfile']['computerName'] = self.short_hostname
            if (self.started and (vm_dict['powerstate'] not in ['starting', 'running']) and self.allocated):
                self.log("CHANGED: virtual machine {0} not running and requested state 'running'".format(self.name))
                changed = True
                powerstate_change = 'poweron'
            elif ((self.state == 'present') and (vm_dict['powerstate'] == 'running') and self.restarted):
                self.log("CHANGED: virtual machine {0} {1} and requested state 'restarted'".format(self.name, vm_dict['powerstate']))
                changed = True
                powerstate_change = 'restarted'
            elif ((self.state == 'present') and (not self.allocated) and (vm_dict['powerstate'] not in ['deallocated', 'deallocating'])):
                self.log("CHANGED: virtual machine {0} {1} and requested state 'deallocated'".format(self.name, vm_dict['powerstate']))
                changed = True
                powerstate_change = 'deallocated'
            elif ((not self.started) and (vm_dict['powerstate'] == 'running')):
                self.log("CHANGED: virtual machine {0} running and requested state 'stopped'".format(self.name))
                changed = True
                powerstate_change = 'poweroff'
            elif (self.generalized and (vm_dict['powerstate'] != 'generalized')):
                self.log("CHANGED: virtual machine {0} requested to be 'generalized'".format(self.name))
                changed = True
                powerstate_change = 'generalized'
            vm_dict['zones'] = ([int(i) for i in vm_dict['zones']] if (('zones' in vm_dict) and vm_dict['zones']) else None)
            if (self.zones != vm_dict['zones']):
                self.log('CHANGED: virtual machine {0} zones'.format(self.name))
                differences.append('Zones')
                changed = True
            if ((self.license_type is not None) and (vm_dict['properties'].get('licenseType') != self.license_type)):
                differences.append('License Type')
                changed = True
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
            default_storage_account = None
            if (not vm):
                self.log('Create virtual machine {0}'.format(self.name))
                self.results['actions'].append('Created VM {0}'.format(self.name))
                if (not self.admin_username):
                    self.fail('Parameter error: admin_username required when creating a virtual machine.')
                if (self.os_type == 'Linux'):
                    if (disable_ssh_password and (not self.ssh_public_keys)):
                        self.fail('Parameter error: ssh_public_keys required when disabling SSH password.')
                if (not image_reference):
                    self.fail('Parameter error: an image is required when creating a virtual machine.')
                availability_set_resource = None
                if self.availability_set:
                    parsed_availability_set = parse_resource_id(self.availability_set)
                    availability_set = self.get_availability_set(parsed_availability_set.get('resource_group', self.resource_group), parsed_availability_set.get('name'))
                    availability_set_resource = self.compute_models.SubResource(id=availability_set.id)
                    if self.zones:
                        self.fail("Parameter error: you can't use Availability Set and Availability Zones at the same time")
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
                    default_storage_account = storage_account
                if (not self.short_hostname):
                    self.short_hostname = self.name
                nics = [self.compute_models.NetworkInterfaceReference(id=id, primary=(i == 0)) for (i, id) in enumerate(network_interfaces)]
                if self.managed_disk_type:
                    vhd = None
                    managed_disk = self.compute_models.ManagedDiskParameters(storage_account_type=self.managed_disk_type)
                elif custom_image:
                    vhd = None
                    managed_disk = None
                else:
                    vhd = self.compute_models.VirtualHardDisk(uri=requested_vhd_uri)
                    managed_disk = None
                plan = None
                if self.plan:
                    plan = self.compute_models.Plan(name=self.plan.get('name'), product=self.plan.get('product'), publisher=self.plan.get('publisher'), promotion_code=self.plan.get('promotion_code'))
                license_type = self.license_type
                vm_resource = self.compute_models.VirtualMachine(location=self.location, tags=self.tags, os_profile=self.compute_models.OSProfile(admin_username=self.admin_username, computer_name=self.short_hostname), hardware_profile=self.compute_models.HardwareProfile(vm_size=self.vm_size), storage_profile=self.compute_models.StorageProfile(os_disk=self.compute_models.OSDisk(name=(self.os_disk_name if self.os_disk_name else self.storage_blob_name), vhd=vhd, managed_disk=managed_disk, create_option=self.compute_models.DiskCreateOptionTypes.from_image, caching=self.os_disk_caching, disk_size_gb=self.os_disk_size_gb), image_reference=image_reference), network_profile=self.compute_models.NetworkProfile(network_interfaces=nics), availability_set=availability_set_resource, plan=plan, zones=self.zones)
                if (self.license_type is not None):
                    vm_resource.license_type = self.license_type
                if self.vm_identity:
                    vm_resource.identity = self.compute_models.VirtualMachineIdentity(type=self.vm_identity)
                if self.winrm:
                    winrm_listeners = list()
                    for winrm_listener in self.winrm:
                        winrm_listeners.append(self.compute_models.WinRMListener(protocol=winrm_listener.get('protocol'), certificate_url=winrm_listener.get('certificate_url')))
                        if winrm_listener.get('source_vault'):
                            if (not vm_resource.os_profile.secrets):
                                vm_resource.os_profile.secrets = list()
                            vm_resource.os_profile.secrets.append(self.compute_models.VaultSecretGroup(source_vault=self.compute_models.SubResource(id=winrm_listener.get('source_vault')), vault_certificates=[self.compute_models.VaultCertificate(certificate_url=winrm_listener.get('certificate_url'), certificate_store=winrm_listener.get('certificate_store'))]))
                    winrm = self.compute_models.WinRMConfiguration(listeners=winrm_listeners)
                    if (not vm_resource.os_profile.windows_configuration):
                        vm_resource.os_profile.windows_configuration = self.compute_models.WindowsConfiguration(win_rm=winrm)
                    elif (not vm_resource.os_profile.windows_configuration.win_rm):
                        vm_resource.os_profile.windows_configuration.win_rm = winrm
                if self.admin_password:
                    vm_resource.os_profile.admin_password = self.admin_password
                if self.custom_data:
                    vm_resource.os_profile.custom_data = to_native(base64.b64encode(to_bytes(self.custom_data)))
                if (self.os_type == 'Linux'):
                    vm_resource.os_profile.linux_configuration = self.compute_models.LinuxConfiguration(disable_password_authentication=disable_ssh_password)
                if self.ssh_public_keys:
                    ssh_config = self.compute_models.SshConfiguration()
                    ssh_config.public_keys = [self.compute_models.SshPublicKey(path=key['path'], key_data=key['key_data']) for key in self.ssh_public_keys]
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
                                data_disk_storage_account = self.get_storage_account(data_disk['storage_account_name'])
                            elif (not default_storage_account):
                                data_disk_storage_account = self.create_default_storage_account()
                                self.log('data disk storage account:')
                                self.log(self.serialize_obj(data_disk_storage_account, 'StorageAccount'), pretty_print=True)
                                default_storage_account = data_disk_storage_account
                            else:
                                data_disk_storage_account = default_storage_account
                            if (not data_disk.get('storage_container_name')):
                                data_disk['storage_container_name'] = 'vhds'
                            data_disk_requested_vhd_uri = 'https://{0}.blob.{1}/{2}/{3}'.format(data_disk_storage_account.name, self._cloud_environment.suffixes.storage_endpoint, data_disk['storage_container_name'], data_disk['storage_blob_name'])
                        if (not data_disk.get('managed_disk_type')):
                            data_disk_managed_disk = None
                            disk_name = data_disk['storage_blob_name']
                            data_disk_vhd = self.compute_models.VirtualHardDisk(uri=data_disk_requested_vhd_uri)
                        else:
                            data_disk_vhd = None
                            data_disk_managed_disk = self.compute_models.ManagedDiskParameters(storage_account_type=data_disk['managed_disk_type'])
                            disk_name = ((self.name + '-datadisk-') + str(count))
                            count += 1
                        data_disk['caching'] = data_disk.get('caching', 'ReadOnly')
                        data_disks.append(self.compute_models.DataDisk(lun=data_disk['lun'], name=disk_name, vhd=data_disk_vhd, caching=data_disk['caching'], create_option=self.compute_models.DiskCreateOptionTypes.empty, disk_size_gb=data_disk['disk_size_gb'], managed_disk=data_disk_managed_disk))
                    vm_resource.storage_profile.data_disks = data_disks
                if (self.accept_terms is True):
                    if ((not self.plan) or (not all([self.plan.get('name'), self.plan.get('product'), self.plan.get('publisher')]))):
                        self.fail('parameter error: plan must be specified and include name, product, and publisher')
                    try:
                        plan_name = self.plan.get('name')
                        plan_product = self.plan.get('product')
                        plan_publisher = self.plan.get('publisher')
                        term = self.marketplace_client.marketplace_agreements.get(publisher_id=plan_publisher, offer_id=plan_product, plan_id=plan_name)
                        term.accepted = True
                        agreement = self.marketplace_client.marketplace_agreements.create(publisher_id=plan_publisher, offer_id=plan_product, plan_id=plan_name, parameters=term)
                    except Exception as exc:
                        self.fail((('Error accepting terms for virtual machine {0} with plan {1}. ' + 'Only service admin/account admin users can purchase images ') + 'from the marketplace. - {2}').format(self.name, self.plan, str(exc)))
                self.log('Create virtual machine with parameters:')
                self.create_or_update_vm(vm_resource, ('all_autocreated' in self.remove_on_absent))
            elif (self.differences and (len(self.differences) > 0)):
                self.log('Update virtual machine {0}'.format(self.name))
                self.results['actions'].append('Updated VM {0}'.format(self.name))
                nics = [self.compute_models.NetworkInterfaceReference(id=interface['id'], primary=(i == 0)) for (i, interface) in enumerate(vm_dict['properties']['networkProfile']['networkInterfaces'])]
                if (not vm_dict['properties']['storageProfile']['osDisk'].get('managedDisk')):
                    managed_disk = None
                    vhd = self.compute_models.VirtualHardDisk(uri=vm_dict['properties']['storageProfile']['osDisk'].get('vhd', {
                        
                    }).get('uri'))
                else:
                    vhd = None
                    managed_disk = self.compute_models.ManagedDiskParameters(storage_account_type=vm_dict['properties']['storageProfile']['osDisk']['managedDisk'].get('storageAccountType'))
                availability_set_resource = None
                try:
                    availability_set_resource = self.compute_models.SubResource(id=vm_dict['properties']['availabilitySet'].get('id'))
                except Exception:
                    pass
                if ('imageReference' in vm_dict['properties']['storageProfile'].keys()):
                    if ('id' in vm_dict['properties']['storageProfile']['imageReference'].keys()):
                        image_reference = self.compute_models.ImageReference(id=vm_dict['properties']['storageProfile']['imageReference']['id'])
                    else:
                        image_reference = self.compute_models.ImageReference(publisher=vm_dict['properties']['storageProfile']['imageReference'].get('publisher'), offer=vm_dict['properties']['storageProfile']['imageReference'].get('offer'), sku=vm_dict['properties']['storageProfile']['imageReference'].get('sku'), version=vm_dict['properties']['storageProfile']['imageReference'].get('version'))
                else:
                    image_reference = None
                if (vm_dict['zones'] != self.zones):
                    self.fail("You can't change the Availability Zone of a virtual machine (have: {0}, want: {1})".format(vm_dict['zones'], self.zones))
                if ('osProfile' in vm_dict['properties']):
                    os_profile = self.compute_models.OSProfile(admin_username=vm_dict['properties'].get('osProfile', {
                        
                    }).get('adminUsername'), computer_name=vm_dict['properties'].get('osProfile', {
                        
                    }).get('computerName'))
                else:
                    os_profile = None
                license_type = None
                if (self.license_type is None):
                    license_type = 'None'
                vm_resource = self.compute_models.VirtualMachine(location=vm_dict['location'], os_profile=os_profile, hardware_profile=self.compute_models.HardwareProfile(vm_size=vm_dict['properties']['hardwareProfile'].get('vmSize')), storage_profile=self.compute_models.StorageProfile(os_disk=self.compute_models.OSDisk(name=vm_dict['properties']['storageProfile']['osDisk'].get('name'), vhd=vhd, managed_disk=managed_disk, create_option=vm_dict['properties']['storageProfile']['osDisk'].get('createOption'), os_type=vm_dict['properties']['storageProfile']['osDisk'].get('osType'), caching=vm_dict['properties']['storageProfile']['osDisk'].get('caching'), disk_size_gb=vm_dict['properties']['storageProfile']['osDisk'].get('diskSizeGB')), image_reference=image_reference), availability_set=availability_set_resource, network_profile=self.compute_models.NetworkProfile(network_interfaces=nics))
                if (self.license_type is not None):
                    vm_resource.license_type = self.license_type
                if vm_dict.get('tags'):
                    vm_resource.tags = vm_dict['tags']
                if vm_dict['properties'].get('osProfile', {
                    
                }).get('customData'):
                    custom_data = vm_dict['properties']['osProfile']['customData']
                    vm_resource.os_profile.custom_data = to_native(base64.b64encode(to_bytes(custom_data)))
                if vm_dict['properties'].get('osProfile', {
                    
                }).get('adminPassword'):
                    vm_resource.os_profile.admin_password = vm_dict['properties']['osProfile']['adminPassword']
                linux_config = vm_dict['properties'].get('osProfile', {
                    
                }).get('linuxConfiguration')
                if linux_config:
                    ssh_config = linux_config.get('ssh', None)
                    vm_resource.os_profile.linux_configuration = self.compute_models.LinuxConfiguration(disable_password_authentication=linux_config.get('disablePasswordAuthentication', False))
                    if ssh_config:
                        public_keys = ssh_config.get('publicKeys')
                        if public_keys:
                            vm_resource.os_profile.linux_configuration.ssh = self.compute_models.SshConfiguration(public_keys=[])
                            for key in public_keys:
                                vm_resource.os_profile.linux_configuration.ssh.public_keys.append(self.compute_models.SshPublicKey(path=key['path'], key_data=key['keyData']))
                if vm_dict['properties']['storageProfile'].get('dataDisks'):
                    data_disks = []
                    for data_disk in vm_dict['properties']['storageProfile']['dataDisks']:
                        if data_disk.get('managedDisk'):
                            managed_disk_type = data_disk['managedDisk'].get('storageAccountType')
                            data_disk_managed_disk = self.compute_models.ManagedDiskParameters(storage_account_type=managed_disk_type)
                            data_disk_vhd = None
                        else:
                            data_disk_vhd = data_disk['vhd']['uri']
                            data_disk_managed_disk = None
                        data_disks.append(self.compute_models.DataDisk(lun=int(data_disk['lun']), name=data_disk.get('name'), vhd=data_disk_vhd, caching=data_disk.get('caching'), create_option=data_disk.get('createOption'), disk_size_gb=int(data_disk['diskSizeGB']), managed_disk=data_disk_managed_disk))
                    vm_resource.storage_profile.data_disks = data_disks
                self.log('Update virtual machine with parameters:')
                self.create_or_update_vm(vm_resource, False)
            if ((powerstate_change == 'poweron') and (self.results['ansible_facts']['azure_vm']['powerstate'] != 'running')):
                self.power_on_vm()
            elif ((powerstate_change == 'poweroff') and (self.results['ansible_facts']['azure_vm']['powerstate'] == 'running')):
                self.power_off_vm()
            elif (powerstate_change == 'restarted'):
                self.restart_vm()
            elif (powerstate_change == 'deallocated'):
                self.deallocate_vm()
            elif (powerstate_change == 'generalized'):
                self.power_off_vm()
                self.generalize_vm()
            self.results['ansible_facts']['azure_vm'] = self.serialize_vm(self.get_vm())
        elif (self.state == 'absent'):
            self.log('Delete virtual machine {0}'.format(self.name))
            self.results['ansible_facts']['azure_vm'] = None
            self.delete_vm(vm)
    del self.results['actions']
    return self.results