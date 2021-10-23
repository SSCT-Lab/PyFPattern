def getfolders(self):
    if (not self.datacenter):
        self.datacenter = find_datacenter_by_name(self.content, self.params['datacenter'])
    if (self.datacenter is None):
        self.module.fail_json(msg=('Unable to find datacenter %(datacenter)s' % self.params))
    self.folders = self._build_folder_tree(self.datacenter.vmFolder)
    self._build_folder_map(self.folders)