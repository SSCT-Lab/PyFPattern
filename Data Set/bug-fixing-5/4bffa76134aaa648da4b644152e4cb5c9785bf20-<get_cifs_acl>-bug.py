def get_cifs_acl(self):
    '\n        Return details about the cifs-share-access-control\n        :param:\n            name : Name of the cifs-share-access-control\n        :return: Details about the cifs-share-access-control. None if not found.\n        :rtype: dict\n        '
    cifs_acl_iter = netapp_utils.zapi.NaElement('cifs-share-access-control-get-iter')
    cifs_acl_info = netapp_utils.zapi.NaElement('cifs-share-access-control')
    cifs_acl_info.add_new_child('share', self.share_name)
    cifs_acl_info.add_new_child('user-or-group', self.user_or_group)
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(cifs_acl_info)
    cifs_acl_iter.add_child_elem(query)
    result = self.server.invoke_successfully(cifs_acl_iter, True)
    return_value = None
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) == 1)):
        cifs_acl = result.get_child_by_name('attributes-list').get_child_by_name('cifs-share-access-control')
        return_value = {
            'share': cifs_acl.get_child_content('share'),
            'user-or-group': cifs_acl.get_child_content('user-or-group'),
            'permission': cifs_acl.get_child_content('permission'),
        }
    return return_value