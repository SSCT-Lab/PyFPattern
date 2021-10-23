@property
def hostvars(self):
    if (self._hostvars != {
        
    }):
        return self._hostvars
    system = 'unknown'
    if ('osProfile' in self._vm_model['properties']):
        if ('linuxConfiguration' in self._vm_model['properties']['osProfile']):
            system = 'linux'
        if ('windowsConfiguration' in self._vm_model['properties']['osProfile']):
            system = 'windows'
    new_hostvars = dict(public_ipv4_addresses=[], public_dns_hostnames=[], private_ipv4_addresses=[], id=self._vm_model['id'], location=self._vm_model['location'], name=self._vm_model['name'], powerstate=self._powerstate, provisioning_state=self._vm_model['properties']['provisioningState'].lower(), tags=self._vm_model.get('tags', {
        
    }), resource_type=self._vm_model.get('type', 'unknown'), vmid=self._vm_model['properties']['vmId'], os_profile=dict(system=system), vmss=(dict(id=self._vmss['id'], name=self._vmss['name']) if self._vmss else {
        
    }), virtual_machine_size=(self._vm_model['properties']['hardwareProfile']['vmSize'] if self._vm_model['properties'].get('hardwareProfile') else None), plan=(self._vm_model['properties']['plan']['name'] if self._vm_model['properties'].get('plan') else None), resource_group=parse_resource_id(self._vm_model['id']).get('resource_group').lower())
    for nic in sorted(self.nics, key=(lambda n: n.is_primary), reverse=True):
        for ipc in sorted(nic._nic_model['properties']['ipConfigurations'], key=(lambda i: i['properties']['primary']), reverse=True):
            private_ip = ipc['properties'].get('privateIPAddress')
            if private_ip:
                new_hostvars['private_ipv4_addresses'].append(private_ip)
            pip_id = ipc['properties'].get('publicIPAddress', {
                
            }).get('id')
            if pip_id:
                new_hostvars['public_ip_id'] = pip_id
                pip = nic.public_ips[pip_id]
                new_hostvars['public_ip_name'] = pip._pip_model['name']
                new_hostvars['public_ipv4_addresses'].append(pip._pip_model['properties'].get('ipAddress', None))
                pip_fqdn = pip._pip_model['properties'].get('dnsSettings', {
                    
                }).get('fqdn')
                if pip_fqdn:
                    new_hostvars['public_dns_hostnames'].append(pip_fqdn)
        new_hostvars['mac_address'] = nic._nic_model['properties'].get('macAddress')
        new_hostvars['network_interface'] = nic._nic_model['name']
        new_hostvars['network_interface_id'] = nic._nic_model['id']
        new_hostvars['security_group_id'] = (nic._nic_model['properties']['networkSecurityGroup']['id'] if nic._nic_model['properties'].get('networkSecurityGroup') else None)
        new_hostvars['security_group'] = (parse_resource_id(new_hostvars['security_group_id'])['resource_name'] if nic._nic_model['properties'].get('networkSecurityGroup') else None)
    new_hostvars['image'] = {
        
    }
    new_hostvars['os_disk'] = {
        
    }
    storageProfile = self._vm_model['properties'].get('storageProfile')
    if storageProfile:
        imageReference = storageProfile.get('imageReference')
        if imageReference:
            if imageReference.get('publisher'):
                new_hostvars['image'] = dict(sku=imageReference.get('sku'), publisher=imageReference.get('publisher'), version=imageReference.get('version'), offer=imageReference.get('offer'))
            elif imageReference.get('id'):
                new_hostvars['image'] = dict(id=imageReference.get('id'))
        osDisk = storageProfile.get('osDisk')
        new_hostvars['os_disk'] = dict(name=osDisk.get('name'), operating_system_type=(osDisk.get('osType').lower() if osDisk.get('osType') else None))
    self._hostvars = new_hostvars
    return self._hostvars