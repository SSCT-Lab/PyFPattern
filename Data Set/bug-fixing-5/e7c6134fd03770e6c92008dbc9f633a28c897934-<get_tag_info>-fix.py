def get_tag_info(self, vm_dynamic_obj):
    vmware_client = VmwareRestClient(self.module)
    return vmware_client.get_tags_for_vm(vm_mid=vm_dynamic_obj._moId)