def _get_zones(self):
    config_zones = self.get_option('regions')
    return set(SCALEWAY_LOCATION.keys()).intersection(config_zones)