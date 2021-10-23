def get_user(self):
    '\n        Checks if the user exists.\n\n        :return:\n            True if user found\n            False if user is not found\n        :rtype: bool\n        '
    security_login_get_iter = netapp_utils.zapi.NaElement('security-login-get-iter')
    query_details = netapp_utils.zapi.NaElement.create_node_with_children('security-login-account-info', **{
        'vserver': self.vserver,
        'user-name': self.name,
        'application': self.application,
        'authentication-method': self.authentication_method,
    })
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(query_details)
    security_login_get_iter.add_child_elem(query)
    return_value = None
    try:
        result = self.server.invoke_successfully(security_login_get_iter, enable_tunneling=False)
        if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) >= 1)):
            interface_attributes = result.get_child_by_name('attributes-list').get_child_by_name('security-login-account-info')
            return_value = {
                'is_locked': interface_attributes.get_child_content('is-locked'),
            }
        return return_value
    except netapp_utils.zapi.NaApiError as error:
        if (to_native(error.code) == '16034'):
            return False
        else:
            self.module.fail_json(msg=('Error getting user %s: %s' % (self.name, to_native(error))), exception=traceback.format_exc())