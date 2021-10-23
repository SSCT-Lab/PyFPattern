def update_check(self, entity):
    res = self._update_check(entity)
    if entity.next_run_configuration_exists:
        res = (res and self._update_check(self._service.service(entity.id).get(next_run=True)))
    return res