def __init__(self, network_id, cluster_network, *args, **kwargs):
    super(ClusterNetworksModule, self).__init__(*args, **kwargs)
    self._network_id = network_id
    self._cluster_network = cluster_network