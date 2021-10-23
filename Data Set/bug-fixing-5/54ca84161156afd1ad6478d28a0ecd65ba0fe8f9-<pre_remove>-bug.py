def pre_remove(self, storage_domain):
    if self._module.params['destroy']:
        return
    self._maintenance(storage_domain)
    self._unattach(storage_domain)