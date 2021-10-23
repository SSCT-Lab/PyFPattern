def parse(self, inventory, loader, path, cache=True):
    super(InventoryModule, self).parse(inventory, loader, path)
    self.config_data = self._read_config_data(path=path)
    self.token = self.get_option('oauth_token')
    for zone in self._get_zones():
        self.do_zone_inventory(zone=zone)