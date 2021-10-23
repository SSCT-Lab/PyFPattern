def add_host(self, host):
    if (host.name not in self._hosts):
        self.hosts.append(host)
        self._hosts.add(host.name)
        host.add_group(self)
        self.clear_hosts_cache()