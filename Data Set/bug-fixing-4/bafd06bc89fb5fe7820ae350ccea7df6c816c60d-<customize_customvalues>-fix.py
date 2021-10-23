def customize_customvalues(self, vm_obj):
    if (len(self.params['customvalues']) == 0):
        return
    facts = self.gather_facts(vm_obj)
    for kv in self.params['customvalues']:
        if (('key' not in kv) or ('value' not in kv)):
            self.module.exit_json(msg="customvalues items required both 'key' and 'value' fields.")
        key_id = None
        for field in self.content.customFieldsManager.field:
            if (field.name == kv['key']):
                key_id = field.key
                break
        if (not key_id):
            self.module.fail_json(msg=('Unable to find custom value key %s' % kv['key']))
        if ((kv['key'] not in facts['customvalues']) or (facts['customvalues'][kv['key']] != kv['value'])):
            self.content.customFieldsManager.SetField(entity=vm_obj, key=key_id, value=kv['value'])
            self.change_detected = True