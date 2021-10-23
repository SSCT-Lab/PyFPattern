

def get_vm(self, vapp_name, vm_name):
    vapp = self.get_vapp(vapp_name)
    vms = [vm for vm in children.get_Vm() if (vm.name == vm_name)]
    try:
        return vms[0]
    except IndexError:
        raise VcaError(('vapp has no vm named %s' % vm_name))
