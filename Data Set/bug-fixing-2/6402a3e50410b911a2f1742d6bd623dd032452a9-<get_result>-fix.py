

def get_result(self, user):
    super(AnsibleCloudStackUser, self).get_result(user)
    if user:
        if ('accounttype' in user):
            for (key, value) in self.account_types.items():
                if (value == user['accounttype']):
                    self.result['account_type'] = key
                    break
        if (self.module.params.get('keys_registered') and ('apikey' in user) and ('secretkey' not in user)):
            user_keys = self.query_api('getUserKeys', id=user['id'])
            if user_keys:
                self.result['user_api_secret'] = user_keys['userkeys'].get('secretkey')
    return self.result
