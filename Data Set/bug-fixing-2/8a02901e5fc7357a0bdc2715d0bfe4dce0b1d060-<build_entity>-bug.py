

def build_entity(self):
    vm = self.param('vm')
    return otypes.VmPool(id=self._module.params['id'], name=self._module.params['name'], description=self._module.params['description'], comment=self._module.params['comment'], cluster=(otypes.Cluster(name=self._module.params['cluster']) if self._module.params['cluster'] else None), template=(otypes.Template(name=self._module.params['template']) if self._module.params['template'] else None), max_user_vms=self._module.params['vm_per_user'], prestarted_vms=self._module.params['prestarted'], size=self._module.params['vm_count'], type=(otypes.VmPoolType(self._module.params['type']) if self._module.params['type'] else None), vm=self.build_vm(vm))
