def __init__(self, module):
    super(PyVmomiHelper, self).__init__(module)
    self.name = self.params['name']
    self.uuid = self.params['uuid']