def parse_sources(self, cache=False):
    ' iterate over inventory sources and parse each one to populate it'
    self._setup_inventory_plugins()
    parsed = False
    for source in self._sources:
        if source:
            if (',' not in source):
                source = unfrackpath(source, follow=False)
            parse = self.parse_source(source, cache=cache)
            if (parse and (not parsed)):
                parsed = True
    if parsed:
        self._inventory.reconcile_inventory()
    elif C.INVENTORY_UNPARSED_IS_FAILED:
        raise AnsibleError('No inventory was parsed, please check your configuration and options.')
    else:
        display.warning('No inventory was parsed, only implicit localhost is available')
    self._inventory_plugins = []