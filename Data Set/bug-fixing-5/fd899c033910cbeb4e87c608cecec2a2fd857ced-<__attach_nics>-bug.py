def __attach_nics(self, entity):
    vnic_profiles_service = self._connection.system_service().vnic_profiles_service()
    nics_service = self._service.service(entity.id).nics_service()
    for nic in self.param('nics'):
        if (search_by_name(nics_service, nic.get('name')) is None):
            if (not self._module.check_mode):
                nics_service.add(otypes.Nic(name=nic.get('name'), interface=otypes.NicInterface(nic.get('interface', 'virtio')), vnic_profile=(otypes.VnicProfile(id=self.__get_vnic_profile_id(nic)) if nic.get('profile_name') else None), mac=(otypes.Mac(address=nic.get('mac_address')) if nic.get('mac_address') else None)))
            self.changed = True