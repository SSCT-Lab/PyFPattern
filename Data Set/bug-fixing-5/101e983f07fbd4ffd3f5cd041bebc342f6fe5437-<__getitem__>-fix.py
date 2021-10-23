def __getitem__(self, varname):
    if (varname not in self._templar._available_variables):
        if (varname in self._locals):
            return self._locals[varname]
        for i in self._extras:
            if (varname in i):
                return i[varname]
        if (varname in self._globals):
            return self._globals[varname]
        else:
            raise KeyError(('undefined variable: %s' % varname))
    variable = self._templar._available_variables[varname]
    from ansible.vars.hostvars import HostVars
    if ((isinstance(variable, dict) and (varname == 'vars')) or isinstance(variable, HostVars) or hasattr(variable, '__UNSAFE__')):
        return variable
    else:
        value = None
        try:
            value = self._templar.template(variable)
        except Exception as e:
            msg = (getattr(e, 'message') or to_native(e))
            raise AnsibleError(("An unhandled exception occurred while templating '%s'. Error was a %s, original message: %s" % (to_native(variable), type(e), msg)))
        return value