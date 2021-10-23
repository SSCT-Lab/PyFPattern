def delete_host_macro(self, host_macro_obj, macro_name):
    host_macro_id = host_macro_obj['hostmacroid']
    try:
        if self._module.check_mode:
            self._module.exit_json(changed=True)
        self._zapi.usermacro.delete([host_macro_id])
        self._module.exit_json(changed=True, result=('Successfully deleted host macro %s ' % macro_name))
    except Exception as e:
        self._module.fail_json(msg=('Failed to delete host macro %s: %s' % (macro_name, e)))