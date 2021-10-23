def getvm_folder_paths(self):
    results = []
    vms = []
    if self.uuid:
        vm_obj = find_vm_by_id(self.content, vm_id=self.uuid, vm_id_type='uuid')
        if (vm_obj is None):
            self.module.fail_json(msg=('Failed to find the virtual machine with UUID : %s' % self.uuid))
        vms = [vm_obj]
    elif self.name:
        objects = self.get_managed_objects_properties(vim_type=vim.VirtualMachine, properties=['name'])
        for temp_vm_object in objects:
            if (temp_vm_object.obj.name == self.name):
                vms.append(temp_vm_object.obj)
    for vm in vms:
        folder_path = self.get_vm_path(self.content, vm)
        results.append(folder_path)
    return results