def _post_start_action(self, entity):
    vm_service = self._service.service(entity.id)
    self._wait_for_UP(vm_service)
    self._attach_cd(vm_service.get())