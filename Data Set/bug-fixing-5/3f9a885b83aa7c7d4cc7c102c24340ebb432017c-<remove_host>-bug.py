def remove_host(self, host):
    self.hosts.remove(host)
    host.remove_group(self)
    self.clear_hosts_cache()