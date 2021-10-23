def delete_vm(self, vm):
    vhd_uris = []
    nic_names = []
    pip_names = []
    if self.remove_on_absent.intersection(set(['all', 'virtual_storage'])):
        self.log('Storing VHD URI for deletion')
        vhd_uris.append(vm.storage_profile.os_disk.vhd.uri)
        data_disks = vm.storage_profile.data_disks
        for data_disk in data_disks:
            vhd_uris.append(data_disk.vhd.uri)
        self.log('VHD URIs to delete: {0}'.format(', '.join(vhd_uris)))
        self.results['deleted_vhd_uris'] = vhd_uris
    if self.remove_on_absent.intersection(set(['all', 'network_interfaces'])):
        self.log('Storing NIC names for deletion.')
        for interface in vm.network_profile.network_interfaces:
            id_dict = azure_id_to_dict(interface.id)
            nic_names.append(id_dict['networkInterfaces'])
        self.log('NIC names to delete {0}'.format(', '.join(nic_names)))
        self.results['deleted_network_interfaces'] = nic_names
        if self.remove_on_absent.intersection(set(['all', 'public_ips'])):
            for name in nic_names:
                nic = self.get_network_interface(name)
                for ipc in nic.ip_configurations:
                    if ipc.public_ip_address:
                        pip_dict = azure_id_to_dict(ipc.public_ip_address.id)
                        pip_names.append(pip_dict['publicIPAddresses'])
            self.log('Public IPs to  delete are {0}'.format(', '.join(pip_names)))
            self.results['deleted_public_ips'] = pip_names
    self.log('Deleting virtual machine {0}'.format(self.name))
    self.results['actions'].append('Deleted virtual machine {0}'.format(self.name))
    try:
        poller = self.compute_client.virtual_machines.delete(self.resource_group, self.name)
        self.get_poller_result(poller)
    except Exception as exc:
        self.fail('Error deleting virtual machine {0} - {1}'.format(self.name, str(exc)))
    if self.remove_on_absent.intersection(set(['all', 'virtual_storage'])):
        self.log('Deleting virtual storage')
        self.delete_vm_storage(vhd_uris)
    if self.remove_on_absent.intersection(set(['all', 'network_interfaces'])):
        self.log('Deleting network interfaces')
        for name in nic_names:
            self.delete_nic(name)
    if self.remove_on_absent.intersection(set(['all', 'public_ips'])):
        self.log('Deleting public IPs')
        for name in pip_names:
            self.delete_pip(name)
    return True