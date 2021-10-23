

def remove_host(self, host):
    if (host.name in self.hosts):
        del self.hosts[host.name]
    for group in self.groups:
        g = self.groups[group]
        g.remove_host(host)
