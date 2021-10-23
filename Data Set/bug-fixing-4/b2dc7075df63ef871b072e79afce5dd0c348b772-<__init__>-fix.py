def __init__(self, module):
    super(VmwareFolderManager, self).__init__(module)
    datacenter_name = self.params.get('datacenter', None)
    self.datacenter_obj = find_datacenter_by_name(self.content, datacenter_name=datacenter_name)
    if (self.datacenter_obj is None):
        self.module.fail_json(msg=('Failed to find datacenter %s' % datacenter_name))
    self.datacenter_folder_type = {
        'vm': self.datacenter_obj.vmFolder,
        'host': self.datacenter_obj.hostFolder,
        'datastore': self.datacenter_obj.datastoreFolder,
        'network': self.datacenter_obj.networkFolder,
    }