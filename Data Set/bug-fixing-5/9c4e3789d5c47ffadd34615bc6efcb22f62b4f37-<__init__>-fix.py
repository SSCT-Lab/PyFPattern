def __init__(self, module):
    self.module = module
    self.account_api_token = module.params['account_api_token']
    self.account_email = module.params['account_email']
    self.algorithm = module.params['algorithm']
    self.cert_usage = module.params['cert_usage']
    self.hash_type = module.params['hash_type']
    self.key_tag = module.params['key_tag']
    self.port = module.params['port']
    self.priority = module.params['priority']
    self.proto = lowercase_string(module.params['proto'])
    self.proxied = module.params['proxied']
    self.selector = module.params['selector']
    self.record = lowercase_string(module.params['record'])
    self.service = lowercase_string(module.params['service'])
    self.is_solo = module.params['solo']
    self.state = module.params['state']
    self.timeout = module.params['timeout']
    self.ttl = module.params['ttl']
    self.type = module.params['type']
    self.value = module.params['value']
    self.weight = module.params['weight']
    self.zone = lowercase_string(module.params['zone'])
    if (self.record == '@'):
        self.record = self.zone
    if ((self.type in ['CNAME', 'NS', 'MX', 'SRV']) and (self.value is not None)):
        self.value = self.value.rstrip('.').lower()
    if ((self.type == 'AAAA') and (self.value is not None)):
        self.value = self.value.lower()
    if (self.type == 'SRV'):
        if ((self.proto is not None) and (not self.proto.startswith('_'))):
            self.proto = ('_' + self.proto)
        if ((self.service is not None) and (not self.service.startswith('_'))):
            self.service = ('_' + self.service)
    if (self.type == 'TLSA'):
        if ((self.proto is not None) and (not self.proto.startswith('_'))):
            self.proto = ('_' + self.proto)
        if (self.port is not None):
            self.port = ('_' + str(self.port))
    if (not self.record.endswith(self.zone)):
        self.record = ((self.record + '.') + self.zone)
    if (self.type == 'DS'):
        if (self.record == self.zone):
            self.module.fail_json(msg='DS records only apply to subdomains.')