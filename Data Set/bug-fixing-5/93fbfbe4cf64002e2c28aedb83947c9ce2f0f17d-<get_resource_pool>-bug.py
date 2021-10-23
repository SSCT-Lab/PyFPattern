def get_resource_pool(self):
    resource_pool = None
    if self.params['resource_pool']:
        resource_pool = self.select_resource_pool_by_name(self.params['resource_pool'])
    elif self.params['esxi_hostname']:
        host = self.select_host()
        resource_pool = self.select_resource_pool_by_host(host)
    elif self.params['cluster']:
        cluster = self.cache.get_cluster(self.params['cluster'])
        resource_pool = cluster.resourcePool
    else:
        resource_pool = self.select_resource_pool_by_name(self.params['resource_pool'])
    if (resource_pool is None):
        self.module.fail_json(msg='Unable to find resource pool, need esxi_hostname, resource_pool, or cluster')
    return resource_pool