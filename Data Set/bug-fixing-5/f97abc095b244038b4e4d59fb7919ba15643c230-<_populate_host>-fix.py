def _populate_host(self, item):
    '\n            :param item: A GCP instance\n        '
    hostname = self._get_hostname(item)
    self.inventory.add_host(hostname)
    for key in item:
        try:
            self.inventory.set_variable(hostname, (self.get_option('vars_prefix') + key), item[key])
        except (ValueError, TypeError) as e:
            self.display.warning(('Could not set host info hostvar for %s, skipping %s: %s' % (hostname, key, to_native(e))))
    self.inventory.add_child('all', hostname)