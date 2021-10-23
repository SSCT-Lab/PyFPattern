def get_export_policy_rule(self):
    '\n        Return details about the export policy rule\n        :param:\n            name : Name of the export_policy\n        :return: Details about the export_policy. None if not found.\n        :rtype: dict\n        '
    (current, result) = (None, None)
    rule_iter = netapp_utils.zapi.NaElement('export-rule-get-iter')
    rule_iter.translate_struct(self.set_query_parameters())
    try:
        result = self.server.invoke_successfully(rule_iter, True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error getting export policy rule %s: %s' % (self.parameters['name'], to_native(error))), exception=traceback.format_exc())
    if ((result is not None) and result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) >= 1)):
        current = dict()
        rule_info = result.get_child_by_name('attributes-list').get_child_by_name('export-rule-info')
        for (item_key, zapi_key) in self.na_helper.zapi_string_keys.items():
            current[item_key] = rule_info.get_child_content(zapi_key)
        for (item_key, zapi_key) in self.na_helper.zapi_bool_keys.items():
            current[item_key] = self.na_helper.get_value_for_bool(from_zapi=True, value=rule_info[zapi_key])
        for (item_key, zapi_key) in self.na_helper.zapi_int_keys.items():
            current[item_key] = self.na_helper.get_value_for_int(from_zapi=True, value=rule_info[zapi_key])
        for (item_key, zapi_key) in self.na_helper.zapi_list_keys.items():
            (parent, dummy) = zapi_key
            current[item_key] = self.na_helper.get_value_for_list(from_zapi=True, zapi_parent=rule_info.get_child_by_name(parent))
        current['num_records'] = int(result.get_child_content('num-records'))
        if (not self.parameters.get('rule_index')):
            self.parameters['rule_index'] = current['rule_index']
    return current