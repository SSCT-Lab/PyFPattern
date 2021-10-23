def getfolders(self):
    if (not self.datacenter):
        self.get_datacenter()
    self.folders = self._build_folder_tree(self.datacenter.vmFolder)
    self._build_folder_map(self.folders)