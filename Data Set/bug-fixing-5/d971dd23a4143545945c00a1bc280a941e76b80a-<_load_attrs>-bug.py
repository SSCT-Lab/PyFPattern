def _load_attrs(self):
    " Turn attribute's value to array. "
    attrs = {
        
    }
    for (name, value) in self.module.params['attributes'].items():
        if (name not in attrs):
            attrs[name] = []
        if isinstance(value, list):
            attrs[name] = value
        else:
            attrs[name].append(str(value))
    return attrs