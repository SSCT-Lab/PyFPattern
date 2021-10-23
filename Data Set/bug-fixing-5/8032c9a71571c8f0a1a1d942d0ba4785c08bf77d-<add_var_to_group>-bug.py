def add_var_to_group(self, group, var, value):
    if (group not in self.inventory.keys()):
        self.inventory[group] = {
            
        }
        self.inventory[group]['hosts'] = []
        self.inventory[group]['vars'] = {
            
        }
    self.inventory[group]['vars'][var] = value