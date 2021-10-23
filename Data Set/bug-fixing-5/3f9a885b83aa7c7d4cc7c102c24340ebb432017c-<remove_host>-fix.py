def remove_host(self, host):
    if (host.name in self._hosts):
        self.hosts.remove(host)
        self._hosts.remove(host.name)
        host.remove_group(self)
        self.clear_hosts_cache()