def _get_zones(self, config_zones):
    return set(SCALEWAY_LOCATION.keys()).intersection(config_zones)