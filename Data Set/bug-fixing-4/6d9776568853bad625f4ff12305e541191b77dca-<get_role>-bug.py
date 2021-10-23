def get_role(self):
    '\n        Checks if the role exists for specific command-directory-name.\n\n        :return:\n            True if role found\n            False if role is not found\n        :rtype: bool\n        '
    security_login_role_get_iter = netapp_utils.zapi.NaElement('security-login-role-get-iter')
    query_details = netapp_utils.zapi.NaElement.create_node_with_children('security-login-role-info', **{
        'vserver': self.vserver,
        'role-name': self.name,
        'command-directory-name': self.command_directory_name,
    })
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(query_details)
    security_login_role_get_iter.add_child_elem(query)
    try:
        result = self.server.invoke_successfully(security_login_role_get_iter, enable_tunneling=False)
    except netapp_utils.zapi.NaApiError as e:
        if (to_native(e.code) == '16031'):
            return False
        else:
            self.module.fail_json(msg=('Error getting role %s: %s' % (self.name, to_native(e))), exception=traceback.format_exc())
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) >= 1)):
        return True
    return False