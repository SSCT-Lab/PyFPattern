def validate_create_parameters(self, keys):
    '\n            Validate if required parameters for create are present.\n            Parameter requirement might vary based on given data-protocol.\n            :return: None\n        '
    if (self.parameters.get('home_node') is None):
        node = self.get_home_node_for_cluster()
        if (node is not None):
            self.parameters['home_node'] = node
    if ((not keys.issubset(set(self.parameters.keys()))) and (self.parameters.get('subnet_name') is None)):
        self.module.fail_json(msg=('Error: Missing one or more required parameters for creating interface: %s' % ', '.join(keys)))
    if ((self.parameters['role'] == 'intercluster') and (self.parameters.get('protocols') is not None)):
        self.module.fail_json(msg='Error: Protocol cannot be specified for intercluster role,failed to create interface')