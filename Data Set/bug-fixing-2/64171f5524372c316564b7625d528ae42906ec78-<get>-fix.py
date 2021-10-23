

def get(self):
    parameters = [param for param in self._exec(['list_parameters', '-p', self.vhost], True) if param.strip()]
    for param_item in parameters:
        (component, name, value) = param_item.split('\t')
        if ((component == self.component) and (name == self.name)):
            self._value = json.loads(value)
            return True
    return False
