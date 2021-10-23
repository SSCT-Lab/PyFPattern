def create_host_macro(self, macro_name, macro_value, host_id):
    try:
        if self._module.check_mode:
            self._module.exit_json(changed=True)
        self._zapi.usermacro.create({
            'hostid': host_id,
            'macro': (('{$' + macro_name) + '}'),
            'value': macro_value,
        })
        self._module.exit_json(changed=True, result=('Successfully added host macro %s' % macro_name))
    except Exception as e:
        self._module.fail_json(msg=('Failed to create host macro %s: %s' % (macro_name, e)))