def getvm(self, name=None, uuid=None, folder=None):
    vm = None
    if uuid:
        vm = find_vm_by_id(self.content, vm_id=uuid, vm_id_type='uuid')
    elif folder:
        searchpath = ('%(folder)s' % self.params)
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