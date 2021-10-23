def _validate_config(self, loader, path):
    '\n            :param loader: an ansible.parsing.dataloader.DataLoader object\n            :param path: the path to the inventory config file\n            :return the contents of the config file\n        '
    if super(InventoryModule, self).verify_file(path):
        if path.endswith(('.aws_ec2.yml' or '.aws_ec2.yaml')):
            return self._read_config_data(path)
    else:
        raise AnsibleParserError('Not a ec2 inventory plugin configuration file')