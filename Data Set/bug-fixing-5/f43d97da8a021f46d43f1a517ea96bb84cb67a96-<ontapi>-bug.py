def ontapi(self):
    api_call = netapp_utils.zapi.NaElement('system-get-ontapi-version')
    try:
        results = self.server.invoke_successfully(api_call, enable_tunneling=False)
        ontapi_version = results.get_child_content('minor-version')
        return ontapi_version
    except netapp_utils.zapi.NaApiError as e:
        self.module.fail_json(msg=('Error calling API %s: %s' % (api_call.to_string(), to_native(e))), exception=traceback.format_exc())