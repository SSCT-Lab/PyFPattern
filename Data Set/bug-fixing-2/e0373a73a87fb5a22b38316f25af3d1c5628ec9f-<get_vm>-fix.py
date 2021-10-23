

def get_vm(self):
    '\n        Find unique virtual machine either by UUID, MoID or Name.\n        Returns: virtual machine object if found, else None.\n\n        '
    vm_obj = None
    user_desired_path = None
    use_instance_uuid = (self.params.get('use_instance_uuid') or False)
    if (('uuid' in self.params) and self.params['uuid']):
        if (not use_instance_uuid):
            vm_obj = find_vm_by_id(self.content, vm_id=self.params['uuid'], vm_id_type='uuid')
        elif use_instance_uuid:
            vm_obj = find_vm_by_id(self.content, vm_id=self.params['uuid'], vm_id_type='instance_uuid')
    elif (('name' in self.params) and self.params['name']):
        objects = self.get_managed_objects_properties(vim_type=vim.VirtualMachine, properties=['name'])
        vms = []
        for temp_vm_object in objects:
            if ((len(temp_vm_object.propSet) == 1) and (temp_vm_object.propSet[0].val == self.params['name'])):
                vms.append(temp_vm_object.obj)
        if (len(vms) > 1):
            if (self.params['folder'] is None):
                self.module.fail_json(msg=('Multiple virtual machines with same name [%s] found, Folder value is a required parameter to find uniqueness of the virtual machine' % self.params['name']), details='Please see documentation of the vmware_guest module for folder parameter.')
            user_folder = self.params['folder']
            user_defined_dc = self.params['datacenter']
            datacenter_obj = find_datacenter_by_name(self.content, self.params['datacenter'])
            dcpath = compile_folder_path_for_object(vobj=datacenter_obj)
            if (not dcpath.endswith('/')):
                dcpath += '/'
            if (user_folder in [None, '', '/']):
                self.module.fail_json(msg=("vmware_guest found multiple virtual machines with same name [%s], please specify folder path other than blank or '/'" % self.params['name']))
            elif user_folder.startswith('/vm/'):
                user_desired_path = ('%s%s%s' % (dcpath, user_defined_dc, user_folder))
            else:
                user_desired_path = user_folder
            for vm in vms:
                actual_vm_folder_path = self.get_vm_path(content=self.content, vm_name=vm)
                if (not actual_vm_folder_path.startswith(('%s%s' % (dcpath, user_defined_dc)))):
                    continue
                if (user_desired_path in actual_vm_folder_path):
                    vm_obj = vm
                    break
        elif vms:
            vm_obj = vms[0]
    elif (('moid' in self.params) and self.params['moid']):
        vm_obj = VmomiSupport.templateOf('VirtualMachine')(self.params['moid'], self.si._stub)
    if vm_obj:
        self.current_vm_obj = vm_obj
    return vm_obj
