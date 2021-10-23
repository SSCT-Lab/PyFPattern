def verify_file(self, path):
    '\n        Verify plugin configuration file and mark this plugin active\n        Args:\n            path: Path of configuration YAML file\n\n        Returns: True if everything is correct, else False\n\n        '
    valid = False
    if super(InventoryModule, self).verify_file(path):
        if path.endswith(('vmware.yaml', 'vmware.yml')):
            valid = True
    return valid