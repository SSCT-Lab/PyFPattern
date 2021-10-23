def update_inventory_mode(self, host_id, inventory_mode):
    if (not inventory_mode):
        return
    if (inventory_mode == 'automatic'):
        inventory_mode = int(1)
    elif (inventory_mode == 'manual'):
        inventory_mode = int(0)
    elif (inventory_mode == 'disabled'):
        inventory_mode = int((- 1))
    request_str = {
        'hostid': host_id,
        'inventory_mode': inventory_mode,
    }
    try:
        if self._module.check_mode:
            self._module.exit_json(changed=True)
        self._zapi.host.update(request_str)
    except Exception as e:
        self._module.fail_json(msg=('Failed to set inventory_mode to host: %s' % e))