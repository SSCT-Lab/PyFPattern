def update_host_macro(self, host_macro_obj, macro_name, macro_value):
    host_macro_id = host_macro_obj['hostmacroid']
    if ((host_macro_obj['macro'] == (('{$' + macro_name) + '}')) and (host_macro_obj['value'] == macro_value)):
        self._module.exit_json(changed=False, result=('Host macro %s already up to date' % macro_name))
    try:
        if self._module.check_mode:
            self._module.exit_json(changed=True)
        self._zapi.usermacro.update({
            'hostmacroid': host_macro_id,
            'value': macro_value,
        })
        self._module.exit_json(changed=True, result=('Successfully updated host macro %s ' % macro_name))
    except Exception as e:
        self._module.fail_json(msg=('Failed to updated host macro %s: %s' % (macro_name, e)))