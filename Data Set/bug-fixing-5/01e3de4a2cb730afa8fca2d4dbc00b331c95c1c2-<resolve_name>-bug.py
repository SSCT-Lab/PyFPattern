def resolve_name(self, modname, parents, path, base):
    if (modname is None):
        if path:
            mod_cls = path.rstrip('.')
        else:
            mod_cls = None
            mod_cls = self.env.temp_data.get('autodoc:class')
            if (mod_cls is None):
                mod_cls = self.env.temp_data.get('py:class')
            if (mod_cls is None):
                return (None, [])
        (modname, accessor) = rpartition(mod_cls, '.')
        (modname, cls) = rpartition(modname, '.')
        parents = [cls, accessor]
        if (not modname):
            modname = self.env.temp_data.get('autodoc:module')
        if (not modname):
            modname = self.env.temp_data.get('py:module')
    return (modname, (parents + [base]))