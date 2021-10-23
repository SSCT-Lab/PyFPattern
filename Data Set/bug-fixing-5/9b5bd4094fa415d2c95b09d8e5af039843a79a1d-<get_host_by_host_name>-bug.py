def get_host_by_host_name(self, host_name):
    host_list = self._zapi.host.get({
        'output': 'extend',
        'filter': {
            'host': [host_name],
        },
    })
    if (len(host_list) < 1):
        self._module.fail_json(msg=('Host not found: %s' % host_name))
    else:
        return host_list[0]