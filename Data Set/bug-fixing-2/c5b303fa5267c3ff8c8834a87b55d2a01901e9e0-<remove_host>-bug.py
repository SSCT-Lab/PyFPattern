

def remove_host(self, host):
    if (host in self.hosts):
        del self.hosts[host]
    for group in self.groups:
        g = self.groups[group]
        g.remove_host(host)
