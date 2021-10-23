def exec_module(self, **kwargs):
    for key in self.module_args:
        setattr(self, key, kwargs[key])
    if (self.name and (not self.resource_group)):
        self.fail('Parameter error: resource group required when filtering by name.')
    if self.name:
        self.results['ansible_facts']['azure_vmss'] = self.get_item()
    else:
        self.results['ansible_facts']['azure_vmss'] = self.list_items()
    if (self.format == 'curated'):
        for index in range(len(self.results['ansible_facts']['azure_vmss'])):
            vmss = self.results['ansible_facts']['azure_vmss'][index]
            subnet_name = None
            load_balancer_name = None
            virtual_network_name = None
            ssh_password_enabled = False
            try:
                subnet_id = vmss['properties']['virtualMachineProfile']['networkProfile']['networkInterfaceConfigurations'][0]['properties']['ipConfigurations'][0]['properties']['subnet']['id']
                subnet_name = re.sub('.*subnets\\/', '', subnet_id)
            except Exception:
                self.log('Could not extract subnet name')
            try:
                backend_address_pool_id = vmss['properties']['virtualMachineProfile']['networkProfile']['networkInterfaceConfigurations'][0]['properties']['ipConfigurations'][0]['properties']['loadBalancerBackendAddressPools'][0]['id']
                load_balancer_name = re.sub('\\/backendAddressPools.*', '', re.sub('.*loadBalancers\\/', '', backend_address_pool_id))
                virtual_network_name = re.sub('.*virtualNetworks\\/', '', re.sub('\\/subnets.*', '', subnet_id))
            except Exception:
                self.log('Could not extract load balancer / virtual network name')
            try:
                ssh_password_enabled = (not vmss['properties']['virtualMachineProfile']['osProfile']['linuxConfiguration']['disablePasswordAuthentication'])
            except Exception:
                self.log('Could not extract SSH password enabled')
            data_disks = vmss['properties']['virtualMachineProfile']['storageProfile'].get('dataDisks', [])
            for disk_index in range(len(data_disks)):
                old_disk = data_disks[disk_index]
                new_disk = {
                    'lun': old_disk['lun'],
                    'disk_size_gb': old_disk['diskSizeGB'],
                    'managed_disk_type': old_disk['managedDisk']['storageAccountType'],
                    'caching': old_disk['caching'],
                }
                data_disks[disk_index] = new_disk
            updated = {
                'id': vmss['id'],
                'resource_group': self.resource_group,
                'name': vmss['name'],
                'state': 'present',
                'location': vmss['location'],
                'vm_size': vmss['sku']['name'],
                'capacity': vmss['sku']['capacity'],
                'tier': vmss['sku']['tier'],
                'upgrade_policy': vmss['properties']['upgradePolicy']['mode'],
                'admin_username': vmss['properties']['virtualMachineProfile']['osProfile']['adminUsername'],
                'admin_password': vmss['properties']['virtualMachineProfile']['osProfile'].get('adminPassword'),
                'ssh_password_enabled': ssh_password_enabled,
                'image': vmss['properties']['virtualMachineProfile']['storageProfile']['imageReference'],
                'os_disk_caching': vmss['properties']['virtualMachineProfile']['storageProfile']['osDisk']['caching'],
                'os_type': ('Linux' if (vmss['properties']['virtualMachineProfile']['osProfile'].get('linuxConfiguration') is not None) else 'Windows'),
                'overprovision': vmss['properties']['overprovision'],
                'managed_disk_type': vmss['properties']['virtualMachineProfile']['storageProfile']['osDisk']['managedDisk']['storageAccountType'],
                'data_disks': data_disks,
                'virtual_network_name': virtual_network_name,
                'subnet_name': subnet_name,
                'load_balancer': load_balancer_name,
                'tags': vmss.get('tags'),
            }
            self.results['ansible_facts']['azure_vmss'][index] = updated
        self.results['vmss'] = self.results['ansible_facts']['azure_vmss']
    return self.results