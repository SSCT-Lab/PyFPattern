def get_list(self, api):
    hostsData = api.host.get({
        'output': 'extend',
        'selectGroups': 'extend',
    })
    data = {
        
    }
    data[self.defaultgroup] = self.hoststub()
    for host in hostsData:
        hostname = host['name']
        data[self.defaultgroup]['hosts'].append(hostname)
        for group in host['groups']:
            groupname = group['name']
            if (groupname not in data):
                data[groupname] = self.hoststub()
            data[groupname]['hosts'].append(hostname)
    return data