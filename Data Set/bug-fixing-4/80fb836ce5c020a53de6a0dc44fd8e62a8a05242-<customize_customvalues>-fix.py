def customize_customvalues(self, vm_obj, config_spec):
    if (len(self.params['customvalues']) == 0):
        return
    vm_custom_spec = config_spec
    vm_custom_spec.extraConfig = []
    changed = False
    facts = self.gather_facts(vm_obj)
    for kv in self.params['customvalues']:
        if (('key' not in kv) or ('value' not in kv)):
            self.module.exit_json(msg="customvalues items required both 'key' and 'value fields.")
        if ((kv['key'] not in facts['customvalues']) or (facts['customvalues'][kv['key']] != kv['value'])):
            option = vim.option.OptionValue()
            option.key = kv['key']
            option.value = kv['value']
            vm_custom_spec.extraConfig.append(option)
            changed = True
    if changed:
        self.change_detected = True