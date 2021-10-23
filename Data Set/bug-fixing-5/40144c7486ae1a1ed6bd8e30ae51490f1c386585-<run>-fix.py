def run(self):
    super(InventoryCLI, self).run()
    results = None
    (self.loader, self.inventory, self.vm) = self._play_prereqs(self.options)
    if self.options.host:
        hosts = self.inventory.get_hosts(self.options.host)
        if (len(hosts) != 1):
            raise AnsibleOptionsError('You must pass a single valid host to --host parameter')
        myvars = self._get_host_variables(host=hosts[0])
        self._remove_internal(myvars)
        results = self.dump(myvars)
    elif self.options.graph:
        results = self.inventory_graph()
    elif self.options.list:
        top = self._get_group('all')
        if self.options.yaml:
            results = self.yaml_inventory(top)
        elif self.options.toml:
            results = self.toml_inventory(top)
        else:
            results = self.json_inventory(top)
        results = self.dump(results)
    if results:
        display.display(results)
        exit(0)
    exit(1)