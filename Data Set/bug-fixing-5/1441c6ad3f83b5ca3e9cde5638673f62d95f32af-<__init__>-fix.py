def __init__(self, network_id, cluster_network, *args, **kwargs):
    super(ClusterNetworksModule, self).__init__(*args, **kwargs)
    self._network_id = network_id
    self._cluster_network = cluster_network
    self._old_usages = []
    self._cluster_network_entity = get_entity(self._service.network_service(network_id))
    if (self._cluster_network_entity is not None):
        self._old_usages = self._cluster_network_entity.usages