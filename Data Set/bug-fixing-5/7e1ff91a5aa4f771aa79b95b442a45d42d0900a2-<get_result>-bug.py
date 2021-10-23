def get_result(self, user):
    super(AnsibleCloudStackUser, self).get_result(user)
    if user:
        if ('accounttype' in user):
            for (key, value) in self.account_types.items():
                if (value == user['accounttype']):
                    self.result['account_type'] = key
                    break
    return self.result