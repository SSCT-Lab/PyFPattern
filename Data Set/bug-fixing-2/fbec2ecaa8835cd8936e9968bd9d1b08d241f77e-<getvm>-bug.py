

def getvm(self, name=None, uuid=None, folder=None, name_match=None, cache=False):
    vm = None
    searchpath = None
    if uuid:
        vm = self.content.searchIndex.FindByUuid(uuid=uuid, vmSearch=True)
    elif folder:
        if self.params['folder'].endswith('/'):
            self.params['folder'] = self.params['folder'][0:(- 1)]
        if self.params['folder'].startswith('/vm'):
            searchpath = ('%s' % self.params['datacenter'])
            searchpath += self.params['folder']
        elif self.params['folder'].startswith('/'):
            searchpath = ('%s' % self.params['datacenter'])
            searchpath += ('/vm' + self.params['folder'])
        else:
            if (not self.folders):
                self.getfolders()
            paths = self.foldermap['paths'].keys()
            paths = [x for x in paths if x.endswith(self.params['folder'])]
            if (len(paths) > 1):
                self.module.fail_json(msg=('%s matches more than one folder. Please use the absolute path starting with /vm/' % self.params['folder']))
            elif paths:
                searchpath = paths[0]
        if searchpath:
            fObj = self.content.searchIndex.FindByInventoryPath(searchpath)
            if fObj:
                if isinstance(fObj, vim.Datacenter):
                    fObj = fObj.vmFolder
                for cObj in fObj.childEntity:
                    if (not isinstance(cObj, vim.VirtualMachine)):
                        continue
                    if (cObj.name == name):
                        vm = cObj
                        break
    if (not vm):
        if folder:
            if (not self.folders):
                self.getfolders()
            vmList = get_all_objs(self.content, [vim.VirtualMachine])
            for item in vmList.items():
                vobj = item[0]
                if (not isinstance(vobj.parent, vim.Folder)):
                    continue
                if (self.compile_folder_path_for_object(vobj) == searchpath):
                    self.current_vm_obj = vobj
                    return vobj
        if name_match:
            if (name_match == 'first'):
                vm = get_obj(self.content, [vim.VirtualMachine], name)
            elif (name_match == 'last'):
                matches = []
                for thisvm in get_all_objs(self.content, [vim.VirtualMachine]):
                    if (thisvm.config.name == name):
                        matches.append(thisvm)
                if matches:
                    vm = matches[(- 1)]
        else:
            matches = []
            for thisvm in get_all_objs(self.content, [vim.VirtualMachine]):
                if (thisvm.config.name == name):
                    matches.append(thisvm)
                if (len(matches) > 1):
                    self.module.fail_json(msg=('more than 1 vm exists by the name %s. Please specify a uuid, or a folder, or a datacenter or name_match' % name))
                if matches:
                    vm = matches[0]
    if (cache and vm):
        self.current_vm_obj = vm
    return vm
