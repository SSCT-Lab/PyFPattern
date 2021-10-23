def __init__(self, **kwargs):
    try:
        import hvac
    except ImportError:
        AnsibleError('Please pip install hvac to use this module')
    self.url = kwargs.pop('url')
    self.secret = kwargs.pop('secret')
    self.token = kwargs.pop('token')
    self.client = hvac.Client(url=self.url, token=self.token)
    if self.client.is_authenticated():
        pass
    else:
        raise AnsibleError('Invalid Hashicorp Vault Token Specified')