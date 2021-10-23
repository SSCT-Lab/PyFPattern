def post_present(self, entity_id):
    entity = self._service.service(entity_id).get()
    self.__attach_disks(entity)
    self.__attach_nics(entity)
    self._attach_cd(entity)
    self.changed = self.__attach_numa_nodes(entity)
    self.changed = self.__attach_watchdog(entity)
    self.changed = self.__attach_graphical_console(entity)