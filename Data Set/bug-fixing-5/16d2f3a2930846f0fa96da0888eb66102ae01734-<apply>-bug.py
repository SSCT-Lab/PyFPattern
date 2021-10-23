def apply(self, data):
    if data.get('stacktrace'):
        self.filter_stacktrace(data['stacktrace'])
    for exc in (get_path(data, 'exception', 'values', filter=True) or ()):
        if exc.get('stacktrace'):
            self.filter_stacktrace(exc['stacktrace'])
    for crumb in (get_path(data, 'breadcrumbs', 'values', filter=True) or ()):
        self.filter_crumb(crumb)
    if data.get('request'):
        self.filter_http(data['request'])
    if data.get('user'):
        self.filter_user(data['user'])
    if data.get('csp'):
        self.filter_csp(data['csp'])
    if data.get('extra'):
        data['extra'] = varmap(self.sanitize, data['extra'])
    if data.get('contexts'):
        for (key, value) in six.iteritems(data['contexts']):
            if value:
                data['contexts'][key] = varmap(self.sanitize, value)