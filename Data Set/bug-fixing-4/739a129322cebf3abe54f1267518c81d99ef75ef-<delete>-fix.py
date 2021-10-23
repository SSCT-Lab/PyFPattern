def delete(self):
    values_to_delete = list(filter(self._is_value_present, self.values))
    if (len(values_to_delete) > 0):
        modlist = [(ldap.MOD_DELETE, self.name, values_to_delete)]
    else:
        modlist = []
    return modlist