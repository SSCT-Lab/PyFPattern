def _populate_host(self, item):
    '\n            :param item: A GCP instance\n        '
    hostname = self._get_hostname(item)
    self.inventory.add_host(hostname)
    for key in item:
        self.inventory.set_variable(hostname, key, item[key])
    self.inventory.add_child('all', hostname)