def add_host(self, host):
    if (host.name not in self.host_names):
        self.hosts.append(host)
        self._hosts.add(host.name)
        host.add_group(self)
        self.clear_hosts_cache()