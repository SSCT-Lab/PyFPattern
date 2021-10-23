def get_igroup(self):
    '\n        Return details about the igroup\n        :param:\n            name : Name of the igroup\n\n        :return: Details about the igroup. None if not found.\n        :rtype: dict\n        '
    igroup_info = netapp_utils.zapi.NaElement('igroup-get-iter')
    igroup_attributes = netapp_utils.zapi.NaElement('initiator-group-info')
    igroup_attributes.add_new_child('initiator-group-name', self.name)
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(igroup_attributes)
    igroup_info.add_child_elem(query)
    result = self.server.invoke_successfully(igroup_info, True)
    return_value = None
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) >= 1)):
        igroup_attributes = result.get_child_by_name('attributes-list').get_child_by_name('igroup-attributes')
        return_value = {
            'name': self.name,
        }
    return return_value