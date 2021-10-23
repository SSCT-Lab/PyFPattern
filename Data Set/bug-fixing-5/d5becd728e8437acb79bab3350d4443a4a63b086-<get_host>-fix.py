def get_host(self):
    host = None
    name = self.module.params.get('name')
    args = {
        'zoneid': self.get_zone(key='id'),
    }
    res = self.cs.listHosts(**args)
    if res:
        for h in res['host']:
            if (name in [h['ipaddress'], h['name']]):
                host = h
    return host