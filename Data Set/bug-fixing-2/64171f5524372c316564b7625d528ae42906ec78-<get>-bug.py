

def get(self):
    parameters = self._exec(['list_parameters', '-p', self.vhost], True)
    for param_item in parameters:
        (component, name, value) = param_item.split('\t')
        if ((component == self.component) and (name == self.name)):
            self._value = json.loads(value)
            return True
    return False
