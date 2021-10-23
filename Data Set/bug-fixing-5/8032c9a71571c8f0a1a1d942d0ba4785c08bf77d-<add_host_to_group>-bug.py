def add_host_to_group(self, group, host):
    if (group not in self.inventory.keys()):
        self.inventory[group] = {
            
        }
        self.inventory[group]['hosts'] = []
        self.inventory[group]['vars'] = {
            
        }
    self.inventory[group]['hosts'].append(host)