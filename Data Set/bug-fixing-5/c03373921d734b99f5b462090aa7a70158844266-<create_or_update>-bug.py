def create_or_update(self, results):
    parameters = self.nsg_models.NetworkSecurityGroup()
    if results.get('rules'):
        parameters.security_rules = []
        for rule in results.get('rules'):
            parameters.security_rules.append(create_rule_instance(self, rule))
    if results.get('default_rules'):
        parameters.default_security_rules = []
        for rule in results.get('default_rules'):
            parameters.default_security_rules.append(create_rule_instance(self, rule))
    parameters.tags = results.get('tags')
    parameters.location = results.get('location')
    try:
        poller = self.client.network_security_groups.create_or_update(resource_group_name=self.resource_group, network_security_group_name=self.name, parameters=parameters)
        result = self.get_poller_result(poller)
    except CloudError as exc:
        self.fail('Error creating/updating security group {0} - {1}'.format(self.name, str(exc)))
    return create_network_security_group_dict(result)