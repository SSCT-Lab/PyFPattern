def get(self, key):
    url = ('%s/%s' % (self.baseurl, key))
    data = None
    value = ''
    try:
        r = open_url(url, validate_certs=self.validate_certs)
        data = r.read()
    except:
        return value
    try:
        item = json.loads(data)
        if (self.version == 'v1'):
            if ('value' in item):
                value = item['value']
        elif ('node' in item):
            value = item['node']['value']
        if ('errorCode' in item):
            value = 'ENOENT'
    except:
        raise
        pass
    return value