def _update_label_assignments(self, entity):
    if (self.param('label') is None):
        return
    labels = [lbl.id for lbl in self._connection.follow_link(entity.network_labels)]
    labels_service = self._service.service(entity.id).network_labels_service()
    if (not (self.param('label') in labels)):
        if (not self._module.check_mode):
            if labels:
                labels_service.label_service(labels[0]).remove()
            labels_service.add(label=otypes.NetworkLabel(id=self.param('label')))
        self.changed = True