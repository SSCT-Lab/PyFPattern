def __init__(self, module):
    super(VMwareHostFactManager, self).__init__(module)
    esxi_host_name = self.params.get('esxi_hostname', None)
    if self.is_vcenter():
        if (esxi_host_name is None):
            self.module.fail_json(msg='Connected to a vCenter system without specifying esxi_hostname')
        self.host = self.get_all_host_objs(esxi_host_name=esxi_host_name)
        if (len(self.host) > 1):
            self.module.fail_json(msg='esxi_hostname matched multiple hosts')
        self.host = self.host[0]
    else:
        self.host = find_obj(self.content, [vim.HostSystem], None)
    if (self.host is None):
        self.module.fail_json(msg='Failed to find host system.')