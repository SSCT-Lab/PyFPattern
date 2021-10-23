def get_lun(self):
    '\n           Check if the LUN exis\n\n        :return: true is it exists, false otherwise\n        :rtype: bool\n        '
    return_value = False
    lun_info = netapp_utils.zapi.NaElement('lun-get-iter')
    query_details = netapp_utils.zapi.NaElement('lun-info')
    query_details.add_new_child('path', self.parameters['destination_path'])
    query_details.add_new_child('vserver', self.parameters['destination_vserver'])
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(query_details)
    lun_info.add_child_elem(query)
    try:
        result = self.server.invoke_successfully(lun_info, True)
    except netapp_utils.zapi.NaApiError as e:
        self.module.fail_json(msg=('Error getting lun  info %s for  verver %s: %s' % (self.parameters['destination_path'], self.parameters['destination_vserver'], to_native(e))), exception=traceback.format_exc())
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) >= 1)):
        return_value = True
    return return_value