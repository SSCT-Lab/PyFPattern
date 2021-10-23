def __init__(self, module):
    super(PyVmomiHelper, self).__init__(module)
    self.datacenter = None
    self.folders = None
    self.name = self.params['name']
    self.uuid = self.params['uuid']