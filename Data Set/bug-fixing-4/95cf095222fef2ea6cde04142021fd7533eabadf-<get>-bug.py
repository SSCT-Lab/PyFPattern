def get(self):
    data = self.client.read(self.secret)
    if (data is None):
        raise AnsibleError(("The secret %s doesn't seem to exist" % self.secret))
    else:
        return data['data']['value']