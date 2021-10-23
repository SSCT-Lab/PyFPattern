def add_host(self, host):
    if (host in self.hosts):
        return
    self.hosts.append(host)
    host.add_group(self)
    self.clear_hosts_cache()