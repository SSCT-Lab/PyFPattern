def pre_remove(self, storage_domain):
    if ((storage_domain.status == sdstate.UNATTACHED) or self._module.params['destroy']):
        return
    self._maintenance(storage_domain)
    self._unattach(storage_domain)