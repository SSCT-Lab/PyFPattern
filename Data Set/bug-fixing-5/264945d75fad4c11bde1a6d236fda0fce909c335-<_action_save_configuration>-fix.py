def _action_save_configuration(self, entity):
    if (not self._module.check_mode):
        self._service.service(entity.id).commit_net_config()
    self.changed = True