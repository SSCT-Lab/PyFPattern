

def commit_changes(self):
    results = netapp_utils.get_cserver(self.server)
    cserver = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=results)
    netapp_utils.ems_log_event('na_ontap_motd', cserver)
    if (self.parameters['state'] == 'absent'):
        self.parameters['message'] = ''
    call = self._create_call()
    try:
        _call_result = self.server.invoke_successfully(call, enable_tunneling=False)
    except netapp_utils.zapi.NaApiError as err:
        self.module.fail_json(msg=('Error calling API %s: %s' % ('vserver-motd-modify-iter', to_native(err))), exception=traceback.format_exc())
    _dict_num_succeeded = xmltodict.parse(_call_result.get_child_by_name('num-succeeded').to_string(), xml_attribs=False)
    num_succeeded = int(_dict_num_succeeded['num-succeeded'])
    changed = bool((num_succeeded >= 1))
    result = {
        'state': self.parameters['state'],
        'changed': changed,
    }
    self.module.exit_json(**result)
