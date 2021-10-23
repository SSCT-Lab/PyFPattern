def get(self, key):
    url = ('%s/%s?recursive=true' % (self.baseurl, key))
    data = None
    value = {
        
    }
    try:
        r = open_url(url, validate_certs=self.validate_certs)
        data = r.read()
    except:
        return None
    try:
        item = json.loads(data)
        if (self.version == 'v1'):
            if ('value' in item):
                value = item['value']
        elif ('node' in item):
            value = self._parse_node(item['node'])
        if ('errorCode' in item):
            value = 'ENOENT'
    except:
        raise
        pass
    return value