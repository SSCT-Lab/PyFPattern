

def select_host(self):
    hostsystem = self.cache.get_esx_host(self.params['esxi_hostname'])
    if (not hostsystem):
        self.module.fail_json(msg=('Failed to find ESX host "%(esxi_hostname)s"' % self.params))
    if ((hostsystem.runtime.connectionState != 'connected') or hostsystem.runtime.inMaintenanceMode):
        self.module.fail_json(msg=('ESXi "%(esxi_hostname)s" is in invalid state or in maintenance mode.' % self.params))
    return hostsystem
