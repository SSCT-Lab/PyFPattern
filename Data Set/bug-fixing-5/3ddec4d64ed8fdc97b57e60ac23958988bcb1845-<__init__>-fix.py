def __init__(self, module):
    self.module = module
    if (module.params['zone'] is None):
        if (module.params['record'][(- 1)] != '.'):
            self.module.fail_json(msg='record must be absolute when omitting zone parameter')
        try:
            self.zone = dns.resolver.zone_for_name(self.module.params['record']).to_text()
        except (dns.exception.Timeout, dns.resolver.NoNameservers, dns.resolver.NoRootSOA) as e:
            self.module.fail_json(msg=('Zone resolver error (%s): %s' % (e.__class__.__name__, to_native(e))))
        if (self.zone is None):
            self.module.fail_json(msg='Unable to find zone, dnspython returned None')
    else:
        self.zone = module.params['zone']
        if (self.zone[(- 1)] != '.'):
            self.zone += '.'
    if (module.params['record'][(- 1)] != '.'):
        self.fqdn = ((module.params['record'] + '.') + self.zone)
    else:
        self.fqdn = module.params['record']
    if module.params['key_name']:
        try:
            self.keyring = dns.tsigkeyring.from_text({
                module.params['key_name']: module.params['key_secret'],
            })
        except TypeError:
            module.fail_json(msg='Missing key_secret')
        except binascii_error as e:
            module.fail_json(msg=('TSIG key error: %s' % to_native(e)))
    else:
        self.keyring = None
    if (module.params['key_algorithm'] == 'hmac-md5'):
        self.algorithm = 'HMAC-MD5.SIG-ALG.REG.INT'
    else:
        self.algorithm = module.params['key_algorithm']
    self.dns_rc = 0