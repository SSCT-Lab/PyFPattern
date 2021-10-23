def call_api(self, call, query=None):
    api_call = netapp_utils.zapi.NaElement(call)
    result = None
    if query:
        for (k, v) in query.items():
            api_call.add_new_child(k, v)
    try:
        result = self.server.invoke_successfully(api_call, enable_tunneling=False)
        return result
    except netapp_utils.zapi.NaApiError as e:
        if (call in ['security-key-manager-key-get-iter']):
            return result
        else:
            self.module.fail_json(msg=('Error calling API %s: %s' % (call, to_native(e))), exception=traceback.format_exc())