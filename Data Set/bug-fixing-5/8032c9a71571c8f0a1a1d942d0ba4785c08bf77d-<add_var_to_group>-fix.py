def add_var_to_group(self, group, var, value):
    clean_group = self.cleanup_group_name(group)
    if (clean_group not in self.inventory.keys()):
        self.inventory[clean_group] = {
            
        }
        self.inventory[clean_group]['hosts'] = []
        self.inventory[clean_group]['vars'] = {
            
        }
    self.inventory[clean_group]['vars'][var] = value