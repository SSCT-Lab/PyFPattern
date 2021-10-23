def getvm_folder_paths(self):
    results = []
    vmList = get_all_objs(self.content, [vim.VirtualMachine])
    for item in vmList.items():
        vobj = item[0]
        if (not isinstance(vobj.parent, vim.Folder)):
            continue
        if ((vobj.config.name == self.name) or (vobj.config.uuid == self.uuid)):
            folderpath = self.get_vm_path(self.content, vobj)
            results.append(folderpath)
    return results