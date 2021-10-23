def parse(self, inventory, loader, path, cache=True):
    super(InventoryModule, self).parse(inventory, loader, path)
    self._read_config_data(path=path)
    config_zones = self.get_option('regions')
    tags = self.get_option('tags')
    token = self.get_option('oauth_token')
    hostname_preference = self.get_option('hostnames')
    for zone in self._get_zones(config_zones):
        self.do_zone_inventory(zone=zone, token=token, tags=tags, hostname_preferences=hostname_preference)