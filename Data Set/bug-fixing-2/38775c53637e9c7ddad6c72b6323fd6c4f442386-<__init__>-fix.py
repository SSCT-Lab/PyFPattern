

def __init__(self, attrs, module):
    self._attributes = attrs
    self._module = module
    self.attr_names = frozenset(self._attributes.keys())
    self._has_key = False
    for (name, attr) in iteritems(self._attributes):
        if attr.get('read_from'):
            spec = self._module.argument_spec.get(attr['read_from'])
            if (not spec):
                raise ValueError(('argument_spec %s does not exist' % attr['read_from']))
            for (key, value) in iteritems(spec):
                if (key not in attr):
                    attr[key] = value
        if attr.get('key'):
            if self._has_key:
                raise ValueError('only one key value can be specified')
            self._has_key = True
            attr['required'] = True
