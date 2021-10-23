def __init__(self, module):
    LdapGeneric.__init__(self, module)
    self.name = self.module.params['name']
    self.state = self.module.params['state']
    if isinstance(self.module.params['values'], list):
        self.values = map(str, self.module.params['values'])
    else:
        self.values = [str(self.module.params['values'])]