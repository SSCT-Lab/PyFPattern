def vmware_path(datastore, datacenter, path):
    ' Constructs a URL path that VSphere accepts reliably '
    path = ('/folder/%s' % path.lstrip('/'))
    datacenter = datacenter.replace('&', '%26')
    if (not path.startswith('/')):
        path = ('/' + path)
    params = dict(dsName=datastore)
    if datacenter:
        params['dcPath'] = datacenter
    params = urlencode(params)
    return ('%s?%s' % (path, params))