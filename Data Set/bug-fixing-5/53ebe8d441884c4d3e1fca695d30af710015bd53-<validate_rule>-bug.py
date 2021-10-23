def validate_rule(rule, rule_type=None):
    "\n    Apply defaults to a rule dictionary and check that all values are valid.\n\n    :param rule: rule dict\n    :param rule_type: Set to 'default' if the rule is part of the default set of rules.\n    :return: None\n    "
    if (not rule.get('name')):
        raise Exception('Rule name value is required.')
    priority = rule.get('priority', None)
    if (not priority):
        raise Exception('Rule priority is required.')
    if (not isinstance(priority, integer_types)):
        raise Exception('Rule priority attribute must be an integer.')
    if ((rule_type != 'default') and ((priority < 100) or (priority > 4096))):
        raise Exception('Rule priority must be between 100 and 4096')
    if (not rule.get('access')):
        rule['access'] = 'Allow'
    access_names = [member.value for member in SecurityRuleAccess]
    if (rule['access'] not in access_names):
        raise Exception('Rule access must be one of [{0}]'.format(', '.join(access_names)))
    if (not rule.get('destination_address_prefix')):
        rule['destination_address_prefix'] = '*'
    if (not rule.get('source_address_prefix')):
        rule['source_address_prefix'] = '*'
    if (not rule.get('protocol')):
        rule['protocol'] = '*'
    protocol_names = [member.value for member in SecurityRuleProtocol]
    if (rule['protocol'] not in protocol_names):
        raise Exception('Rule protocol must be one of [{0}]'.format(', '.join(protocol_names)))
    if (not rule.get('direction')):
        rule['direction'] = 'Inbound'
    direction_names = [member.value for member in SecurityRuleDirection]
    if (rule['direction'] not in direction_names):
        raise Exception('Rule direction must be one of [{0}]'.format(', '.join(direction_names)))
    if (not rule.get('source_port_range')):
        rule['source_port_range'] = '*'
    if (not rule.get('destination_port_range')):
        rule['destination_port_range'] = '*'