def delete_proxy(self, proxy_id, proxy_name):
    try:
        if self._module.check_mode:
            self._zapi.logout()
            self._module.exit_json(changed=True)
        self._zapi.proxy.delete([proxy_id])
        self._zapi.logout()
        self._module.exit_json(changed=True, result=('Successfully deleted' + (' proxy %s' % proxy_name)))
    except Exception as e:
        self._zapi.logout()
        self._module.fail_json(msg=('Failed to delete proxy %s: %s' % (proxy_name, str(e))))