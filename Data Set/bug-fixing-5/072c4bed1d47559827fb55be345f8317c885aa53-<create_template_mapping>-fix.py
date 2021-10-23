def create_template_mapping(self, inventory, pattern, dtype='string'):
    ' Return a hash of uuid to templated string from pattern '
    mapping = {
        
    }
    for (k, v) in inventory['_meta']['hostvars'].iteritems():
        t = jinja2.Template(pattern)
        newkey = None
        try:
            newkey = t.render(v)
            newkey = newkey.strip()
        except Exception as e:
            self.debugl(e)
        if (not newkey):
            continue
        elif (dtype == 'integer'):
            newkey = int(newkey)
        elif (dtype == 'boolean'):
            if (newkey.lower() == 'false'):
                newkey = False
            elif (newkey.lower() == 'true'):
                newkey = True
        elif (dtype == 'string'):
            pass
        mapping[k] = newkey
    return mapping