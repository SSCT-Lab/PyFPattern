

def get_host_info(self, host):
    ' Return hostvars for a single host '
    if (host in self.inventory['_meta']['hostvars']):
        return self.inventory['_meta']['hostvars'][host]
    elif (self.args.host and self.inventory['_meta']['hostvars']):
        match = None
        for (k, v) in self.inventory['_meta']['hostvars'].items():
            if (self.inventory['_meta']['hostvars'][k]['name'] == self.args.host):
                match = k
                break
        if match:
            return self.inventory['_meta']['hostvars'][match]
        else:
            raise VMwareMissingHostException(('%s not found' % host))
    else:
        raise VMwareMissingHostException(('%s not found' % host))
