

def create_rule_instance(self, rule):
    '\n    Create an instance of SecurityRule from a dict.\n\n    :param rule: dict\n    :return: SecurityRule\n    '
    return self.network_models.SecurityRule(protocol=rule['protocol'], source_address_prefix=rule['source_address_prefix'], destination_address_prefix=rule['destination_address_prefix'], access=rule['access'], direction=rule['direction'], id=rule.get('id', None), description=rule.get('description', None), source_port_range=rule.get('source_port_range', None), destination_port_range=rule.get('destination_port_range', None), priority=rule.get('priority', None), provisioning_state=rule.get('provisioning_state', None), name=rule.get('name', None), etag=rule.get('etag', None))
