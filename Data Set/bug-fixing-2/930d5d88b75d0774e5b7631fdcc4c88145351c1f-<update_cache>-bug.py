

def update_cache(self):
    ' Make calls to cobbler and save the output in a cache '
    self._connect()
    self.groups = dict()
    self.hosts = dict()
    if (self.token is not None):
        data = self.conn.get_systems(self.token)
    else:
        data = self.conn.get_systems()
    for host in data:
        dns_name = host['hostname']
        ksmeta = None
        interfaces = host['interfaces']
        if (dns_name == ''):
            for (iname, ivalue) in iteritems(interfaces):
                if (ivalue['management'] or (not ivalue['static'])):
                    this_dns_name = ivalue.get('dns_name', None)
                    if ((this_dns_name is not None) and (this_dns_name is not '')):
                        dns_name = this_dns_name
        if (dns_name == ''):
            continue
        status = host['status']
        profile = host['profile']
        classes = host[orderby_keyname]
        if (status not in self.inventory):
            self.inventory[status] = []
        self.inventory[status].append(dns_name)
        if (profile not in self.inventory):
            self.inventory[profile] = []
        self.inventory[profile].append(dns_name)
        for cls in classes:
            if (cls not in self.inventory):
                self.inventory[cls] = []
            self.inventory[cls].append(dns_name)
        self.cache[dns_name] = host
        if ('ks_meta' in host):
            for (key, value) in iteritems(host['ks_meta']):
                self.cache[dns_name][key] = value
    self.write_to_cache(self.cache, self.cache_path_cache)
    self.write_to_cache(self.inventory, self.cache_path_inventory)
