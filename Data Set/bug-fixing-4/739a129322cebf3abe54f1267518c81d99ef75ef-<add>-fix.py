def add(self):
    values_to_add = list(filter(self._is_value_absent, self.values))
    if (len(values_to_add) > 0):
        modlist = [(ldap.MOD_ADD, self.name, values_to_add)]
    else:
        modlist = []
    return modlist