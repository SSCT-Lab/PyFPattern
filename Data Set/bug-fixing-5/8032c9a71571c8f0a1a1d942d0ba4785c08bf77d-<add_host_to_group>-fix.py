def add_host_to_group(self, group, host):
    clean_group = self.cleanup_group_name(group)
    if (clean_group not in self.inventory.keys()):
        self.inventory[clean_group] = {
            
        }
        self.inventory[clean_group]['hosts'] = []
        self.inventory[clean_group]['vars'] = {
            
        }
    self.inventory[clean_group]['hosts'].append(host)