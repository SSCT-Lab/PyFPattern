def _inventory_group(self, group, contents):
    "Takes a group and returns inventory for it as dict\n\n        :param group: Group name\n        :type group: str\n        :param contents: The contents of the group's YAML config\n        :type contents: dict\n\n        contents param should look like::\n\n            {\n              'query': 'xx',\n              'vars':\n                  'a': 'b'\n            }\n\n        Will return something like::\n\n            { group: {\n                hosts: [],\n                vars: {},\n            }\n        "
    query = contents.get('query')
    hostvars = contents.get('vars', dict())
    site = contents.get('site', dict())
    obj = {
        group: dict(),
    }
    obj[group]['hosts'] = []
    obj[group]['vars'] = hostvars
    try:
        assert isinstance(query, string_types)
    except:
        sys.exit(('ERR: Group queries must be a single string\n  Group: %s\n  Query: %s\n' % (group, query)))
    try:
        if site:
            site = self.client.sites(site)
            devices = site.devices.query.get(query=query)
        else:
            devices = self.client.devices.query.get(query=query)
    except HttpServerError as e:
        if ('500' in str(e.response)):
            _site = 'Correct site id?'
            _attr = 'Queried attributes actually exist?'
            questions = ((_site + '\n') + _attr)
            sys.exit(('ERR: 500 from server.\n%s' % questions))
        else:
            raise
    except UsageError:
        sys.exit('ERR: Could not connect to server. Running?')
    for host in devices['data']['devices']:
        hostname = host['hostname']
        obj[group]['hosts'].append(hostname)
        attributes = host['attributes']
        attributes.update({
            'site_id': host['site_id'],
            'id': host['id'],
        })
        self._meta['hostvars'].update({
            hostname: attributes,
        })
    return obj