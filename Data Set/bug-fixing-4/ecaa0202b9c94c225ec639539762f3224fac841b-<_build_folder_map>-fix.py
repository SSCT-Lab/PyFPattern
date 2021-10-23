def _build_folder_map(self, folder, inpath='/'):
    ' Build a searchable index for vms+uuids+folders '
    if isinstance(folder, tuple):
        folder = folder[1]
    if (inpath == '/'):
        thispath = '/vm'
    else:
        thispath = os.path.join(inpath, folder['name'])
    if (thispath not in self.foldermap['paths']):
        self.foldermap['paths'][thispath] = []
    self.foldermap['fvim_by_path'][thispath] = folder['vimobj']
    self.foldermap['path_by_fvim'][folder['vimobj']] = thispath
    for item in folder.items():
        k = item[0]
        v = item[1]
        if (k == 'name'):
            pass
        elif (k == 'subfolders'):
            for x in v.items():
                self._build_folder_map(x, inpath=thispath)
        elif (k == 'virtualmachines'):
            for x in v:
                if (x.config is None):
                    continue
                self.foldermap['uuids'][x.config.uuid] = x.config.name
                self.foldermap['paths'][thispath].append(x.config.uuid)
                if (x not in self.foldermap['path_by_vvim']):
                    self.foldermap['path_by_vvim'][x] = thispath