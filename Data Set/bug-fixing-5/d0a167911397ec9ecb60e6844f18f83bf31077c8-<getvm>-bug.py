def getvm(self, name=None, uuid=None, folder=None):
    vm = None
    if uuid:
        vm = find_vm_by_id(self.content, vm_id=uuid, vm_id_type='uuid')
    elif folder:
        if (not self.params['folder'].startswith('/')):
            self.module.fail_json(msg=("Folder %(folder)s needs to be an absolute path, starting with '/'." % self.params))
        searchpath = ('%(datacenter)s%(folder)s' % self.params)
        f_obj = self.content.searchIndex.FindByInventoryPath(searchpath)
        if f_obj:
            if isinstance(f_obj, vim.Datacenter):
                f_obj = f_obj.vmFolder
            for c_obj in f_obj.childEntity:
                if (not isinstance(c_obj, vim.VirtualMachine)):
                    continue
                if (c_obj.name == name):
                    vm = c_obj
                    if (self.params['name_match'] == 'first'):
                        break
    return vm