def __init__(self, **kwargs):
    try:
        import hvac
    except ImportError:
        raise AnsibleError('Please pip install hvac to use this module')
    self.url = kwargs.get('url', ANSIBLE_HASHI_VAULT_ADDR)
    self.token = kwargs.get('token')
    if (self.token == None):
        raise AnsibleError('No Vault Token specified')
    s = kwargs.get('secret')
    if (s == None):
        raise AnsibleError('No secret specified')
    s_f = s.split(':')
    self.secret = s_f[0]
    if (len(s_f) >= 2):
        self.secret_field = s_f[1]
    else:
        self.secret_field = 'value'
    self.client = hvac.Client(url=self.url, token=self.token)
    if self.client.is_authenticated():
        pass
    else:
        raise AnsibleError('Invalid Hashicorp Vault Token Specified')