def get_proxyid_by_proxy_name(self, proxy_name):
    proxy_list = self._zapi.proxy.get({
        'output': 'extend',
        'filter': {
            'host': [proxy_name],
        },
    })
    if (len(proxy_list) < 1):
        self._module.fail_json(msg=('Proxy not found: %s' % proxy_name))
    else:
        return int(proxy_list[0]['proxyid'])