def get(self):
    data = self.client.read(self.secret)
    if (data is None):
        raise AnsibleError(("The secret %s doesn't seem to exist for hashi_vault lookup" % self.secret))
    if (self.secret_field == ''):
        return data['data']
    if (self.secret_field not in data['data']):
        raise AnsibleError(("The secret %s does not contain the field '%s'. for hashi_vault lookup" % (self.secret, self.secret_field)))
    return data['data'][self.secret_field]