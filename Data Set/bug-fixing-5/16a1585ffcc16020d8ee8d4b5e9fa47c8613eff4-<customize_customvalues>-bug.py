def customize_customvalues(self, vm_obj):
    if (len(self.params['customvalues']) == 0):
        return
    facts = self.gather_facts(vm_obj)
    for kv in self.params['customvalues']:
        if (('key' not in kv) or ('value' not in kv)):
            self.module.exit_json(msg="customvalues items required both 'key' and 'value fields.")
        if ((kv['key'] in facts['customvalues']) and (facts['customvalues'][kv['key']] != kv['value'])):
            try:
                vm_obj.setCustomValue(key=kv['key'], value=kv['value'])
                self.change_detected = True
            except Exception:
                e = get_exception()
                self.module.fail_json(msg=("Failed to set custom value for key='%s' and value='%s'. Error was: %s" % (kv['key'], kv['value'], e)))