

def _setup_inventory_plugins(self):
    ' sets up loaded inventory plugins for usage '
    inventory_loader = PluginLoader('InventoryModule', 'ansible.plugins.inventory', C.DEFAULT_INVENTORY_PLUGIN_PATH, 'inventory_plugins')
    display.vvvv('setting up inventory plugins')
    for name in C.INVENTORY_ENABLED:
        plugin = inventory_loader.get(name)
        if plugin:
            self._inventory_plugins.append(plugin)
        else:
            display.warning(('Failed to load inventory plugin, skipping %s' % name))
    if (not self._inventory_plugins):
        raise AnsibleError('No inventory plugins available to generate inventory, make sure you have at least one whitelisted.')
