def _get_network_filter(self):
    network_filter = None
    if self.param('network_filter'):
        network_filter = otypes.NetworkFilter(id=self._get_network_filter_id())
    elif ((self.param('network_filter') == '') or (self.param('pass_through') == 'enabled')):
        network_filter = otypes.NetworkFilter()
    return network_filter