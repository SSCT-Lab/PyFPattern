def run(self):
    results = None
    super(InventoryCLI, self).run()
    if getattr(self, '_play_prereqs', False):
        (self.loader, self.inventory, self.vm) = self._play_prereqs(self.options)
    else:
        from ansible.vars import VariableManager
        from ansible.inventory import Inventory
        self._new_api = False
        self.loader = DataLoader()
        self.vm = VariableManager()
        if self.options.vault_password_file:
            vault_pass = CLI.read_vault_password_file(self.options.vault_password_file, loader=self.loader)
        elif self.options.ask_vault_pass:
            vault_pass = self.ask_vault_passwords()
        else:
            vault_pass = None
        if vault_pass:
            self.loader.set_vault_password(vault_pass)
        self.inventory = Inventory(loader=self.loader, variable_manager=self.vm, host_list=self.options.inventory)
        self.vm.set_inventory(self.inventory)
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