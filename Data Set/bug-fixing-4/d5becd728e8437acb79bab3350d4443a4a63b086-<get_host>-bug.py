def get_host(self):
    host = None
    args = {
        'zoneid': self.get_zone(key='id'),
        'name': self.module.params.get('name'),
    }
    hosts = self.cs.listHosts(**args)
    if hosts:
        host = hosts['host'][0]
    return host