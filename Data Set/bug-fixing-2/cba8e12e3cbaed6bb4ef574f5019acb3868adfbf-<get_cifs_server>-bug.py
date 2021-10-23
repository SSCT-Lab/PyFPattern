

def get_cifs_server(self):
    '\n        Return details about the CIFS-server\n        :param:\n            name : Name of the name of the cifs_server\n\n        :return: Details about the cifs_server. None if not found.\n        :rtype: dict\n        '
    cifs_server_info = netapp_utils.zapi.NaElement('cifs-server-get-iter')
    cifs_server_attributes = netapp_utils.zapi.NaElement('cifs-server-config')
    cifs_server_attributes.add_new_child('cifs-server', self.cifs_server_name)
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(cifs_server_attributes)
    cifs_server_info.add_child_elem(query)
    result = self.server.invoke_successfully(cifs_server_info, True)
    return_value = None
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) >= 1)):
        cifs_server_attributes = result.get_child_by_name('attributes-list').get_child_by_name('cifs-server-config')
        return_value = {
            'cifs_server_name': self.cifs_server_name,
            'administrative-status': cifs_server_attributes.get_child_content('administrative-status'),
        }
    return return_value
