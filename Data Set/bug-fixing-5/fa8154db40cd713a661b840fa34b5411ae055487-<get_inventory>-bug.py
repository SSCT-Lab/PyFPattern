def get_inventory(self):
    if (len(self.resource_groups) > 0):
        for resource_group in self.resource_groups:
            try:
                virtual_machines = self._compute_client.virtual_machines.list(resource_group)
            except Exception as exc:
                sys.exit('Error: fetching virtual machines for resource group {0} - {1}'.format(resource_group, str(exc)))
            if (self._args.host or self.tags):
                selected_machines = self._selected_machines(virtual_machines)
                self._load_machines(selected_machines)
            else:
                self._load_machines(virtual_machines)
    else:
        try:
            virtual_machines = self._compute_client.virtual_machines.list_all()
        except Exception as exc:
            sys.exit('Error: fetching virtual machines - {0}'.format(str(exc)))
        if (self._args.host or self.tags or self.locations):
            selected_machines = self._selected_machines(virtual_machines)
            self._load_machines(selected_machines)
        else:
            self._load_machines(virtual_machines)