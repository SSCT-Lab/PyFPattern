def remove_custom_def(self, field):
    changed = False
    f = dict()
    for x in self.custom_field_mgr:
        if ((x.name == field) and (x.managedObjectType == vim.VirtualMachine)):
            changed = True
            if (not self.module.check_mode):
                self.content.customFieldsManager.RemoveCustomFieldDef(key=x.key)
                break
        f[x.name] = (x.key, x.managedObjectType)
    return {
        'changed': changed,
        'failed': False,
        'custom_attribute_defs': list(f.keys()),
    }