def unlock_given_user(self):
    '\n        unlocks the user\n\n        :return:\n            True if user unlocked\n            False if unlock user is not performed\n        :rtype: bool\n        '
    user_unlock = netapp_utils.zapi.NaElement.create_node_with_children('security-login-unlock', **{
        'vserver': self.vserver,
        'user-name': self.name,
    })
    try:
        self.server.invoke_successfully(user_unlock, enable_tunneling=False)
    except netapp_utils.zapi.NaApiError as error:
        if (to_native(error.code) == '13114'):
            return False
        else:
            self.module.fail_json(msg=('Error unlocking user %s: %s' % (self.name, to_native(error))), exception=traceback.format_exc())
    return True