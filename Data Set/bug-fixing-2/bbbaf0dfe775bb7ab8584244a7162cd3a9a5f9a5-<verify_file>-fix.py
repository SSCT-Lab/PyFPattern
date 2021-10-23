

def verify_file(self, path):
    '\n        Verify plugin configuration file and mark this plugin active\n        Args:\n            path: Path of configuration YAML file\n        Returns: True if everything is correct, else False\n        '
    valid = False
    if super(InventoryModule, self).verify_file(path):
        if path.endswith(('vmware.yaml', 'vmware.yml', 'vmware_vm_inventory.yaml', 'vmware_vm_inventory.yml')):
            valid = True
    return valid
