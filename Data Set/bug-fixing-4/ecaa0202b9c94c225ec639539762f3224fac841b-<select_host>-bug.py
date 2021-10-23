def select_host(self):
    if self.params['cluster']:
        cluster = self.cache.get_cluster(self.params['cluster'])
        if (not cluster):
            self.module.fail_json(msg=('Failed to find a cluster named %s' % self.params['cluster']))
        hostsystems = [x for x in cluster.host]
        hostsystem = hostsystems[0]
    else:
        hostsystem = self.cache.get_esx_host(self.params['esxi_hostname'])
        if (not hostsystem):
            self.module.fail_json(msg=('Failed to find a host named %s' % self.params['esxi_hostname']))
    return hostsystem