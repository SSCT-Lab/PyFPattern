@property
def hostvars(self):
    if (self._hostvars != {
        
    }):
        return self._hostvars
    new_hostvars = dict(public_ipv4_addresses=[], public_dns_hostnames=[], private_ipv4_addresses=[], id=self._vm_model['id'], location=self._vm_model['location'], name=self._vm_model['name'], powerstate=self._powerstate, provisioning_state=self._vm_model['properties']['provisioningState'].lower(), tags=self._vm_model.get('tags', {
        
    }), resource_type=self._vm_model.get('type', 'unknown'), vmid=self._vm_model['properties']['vmId'], vmss=(dict(id=self._vmss['id'], name=self._vmss['name']) if self._vmss else {
        
    }))
    for nic in sorted(self.nics, key=(lambda n: n.is_primary), reverse=True):
        for ipc in sorted(nic._nic_model['properties']['ipConfigurations'], key=(lambda i: i['properties']['primary']), reverse=True):
            private_ip = ipc['properties'].get('privateIPAddress')
            if private_ip:
                new_hostvars['private_ipv4_addresses'].append(private_ip)
            pip_id = ipc['properties'].get('publicIPAddress', {
                
            }).get('id')
            if pip_id:
                pip = nic.public_ips[pip_id]
                new_hostvars['public_ipv4_addresses'].append(pip._pip_model['properties'].get('ipAddress', None))
                pip_fqdn = pip._pip_model['properties'].get('dnsSettings', {
                    
                }).get('fqdn')
                if pip_fqdn:
                    new_hostvars['public_dns_hostnames'].append(pip_fqdn)
    self._hostvars = new_hostvars
    return self._hostvars