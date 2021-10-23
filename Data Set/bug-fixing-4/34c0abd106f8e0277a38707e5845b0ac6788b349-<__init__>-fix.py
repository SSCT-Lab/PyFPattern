def __init__(self, module):
    self.state = module.params['state']
    self.digest = module.params['digest']
    self.force = module.params['force']
    self.subjectAltName = module.params['subjectAltName']
    self.path = module.params['path']
    self.privatekey_path = module.params['privatekey_path']
    self.version = module.params['version']
    self.changed = True
    self.request = None
    self.privatekey = None
    self.subject = {
        'C': module.params['countryName'],
        'ST': module.params['stateOrProvinceName'],
        'L': module.params['localityName'],
        'O': module.params['organizationName'],
        'OU': module.params['organizationalUnitName'],
        'CN': module.params['commonName'],
        'emailAddress': module.params['emailAddress'],
    }
    if (self.subjectAltName is None):
        self.subjectAltName = ('DNS:%s' % self.subject['CN'])
    self.subject = dict(((k, v) for (k, v) in self.subject.items() if v))