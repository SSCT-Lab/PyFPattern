

def __init__(self, module):
    super(ExoDnsRecord, self).__init__(module)
    self.content = self.module.params.get('content')
    if self.content:
        self.content = self.content.lower()
    self.domain = self.module.params.get('domain').lower()
    self.name = self.module.params.get('name').lower()
    if (self.name == self.domain):
        self.name = ''
    self.multiple = self.module.params.get('multiple')
    self.record_type = self.module.params.get('record_type')
    if (self.multiple and (self.record_type != 'A')):
        self.module.fail_json(msg='Multiple is only usable with record_type A')
