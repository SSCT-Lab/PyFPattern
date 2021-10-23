def __init__(self, **kwargs):
    self.url = kwargs.get('url', ANSIBLE_HASHI_VAULT_ADDR)
    s = kwargs.get('secret')
    if (s is None):
        raise AnsibleError('No secret specified for hashi_vault lookup')
    s_f = s.rsplit(':', 1)
    self.secret = s_f[0]
    if (len(s_f) >= 2):
        self.secret_field = s_f[1]
    else:
        self.secret_field = ''
    self.verify = self.boolean_or_cacert(kwargs.get('validate_certs', True), kwargs.get('cacert', ''))
    self.auth_method = kwargs.get('auth_method')
    if (self.auth_method and (self.auth_method != 'token')):
        try:
            self.client = hvac.Client(url=self.url, verify=self.verify)
            getattr(self, ('auth_' + self.auth_method))(**kwargs)
        except AttributeError:
            raise AnsibleError(("Authentication method '%s' not supported" % self.auth_method))
    else:
        self.token = kwargs.get('token', os.environ.get('VAULT_TOKEN', None))
        if ((self.token is None) and os.environ.get('HOME')):
            token_filename = os.path.join(os.environ.get('HOME'), '.vault-token')
            if os.path.exists(token_filename):
                with open(token_filename) as token_file:
                    self.token = token_file.read().strip()
        if (self.token is None):
            raise AnsibleError('No Vault Token specified')
        self.client = hvac.Client(url=self.url, token=self.token, verify=self.verify)
    if (not self.client.is_authenticated()):
        raise AnsibleError('Invalid Hashicorp Vault Token Specified for hashi_vault lookup')