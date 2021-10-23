def get_export_policy(self, name=None):
    '\n        Return details about the export-policy\n        :param:\n            name : Name of the export-policy\n        :return: Details about the export-policy. None if not found.\n        :rtype: dict\n        '
    if (name is None):
        name = self.name
    export_policy_iter = netapp_utils.zapi.NaElement('export-policy-get-iter')
    export_policy_info = netapp_utils.zapi.NaElement('export-policy-info')
    export_policy_info.add_new_child('policy-name', name)
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(export_policy_info)
    export_policy_iter.add_child_elem(query)
    result = self.server.invoke_successfully(export_policy_iter, True)
    return_value = None
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) == 1)):
        export_policy = result.get_child_by_name('attributes-list').get_child_by_name('export-policy-info').get_child_by_name('policy-name')
        return_value = {
            'policy-name': export_policy,
        }
    return return_value