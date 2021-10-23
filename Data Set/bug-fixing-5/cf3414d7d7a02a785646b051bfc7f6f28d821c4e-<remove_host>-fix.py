def remove_host(self, host):
    if (host.name in self.host_names):
        self.hosts.remove(host)
        self._hosts.remove(host.name)
        host.remove_group(self)
        self.clear_hosts_cache()