def run(self, terms, variables=None, **kwargs):
    if (variables is not None):
        self._templar.set_available_variables(variables)
    myvars = getattr(self._templar, '_available_variables', {
        
    })
    self.set_options(direct=kwargs)
    default = self.get_option('default')
    ret = []
    for term in terms:
        if (not isinstance(term, string_types)):
            raise AnsibleError(('Invalid setting identifier, "%s" is not a string, its a %s' % (term, type(term))))
        try:
            try:
                value = myvars[term]
            except KeyError:
                try:
                    value = myvars['hostvars'][myvars['inventory_hostname']][term]
                except KeyError:
                    raise AnsibleUndefinedVariable(('No variable found with this name: %s' % term))
            ret.append(self._templar.template(value, fail_on_undefined=True))
        except AnsibleUndefinedVariable:
            if (default is not None):
                ret.append(default)
            else:
                raise
    return ret