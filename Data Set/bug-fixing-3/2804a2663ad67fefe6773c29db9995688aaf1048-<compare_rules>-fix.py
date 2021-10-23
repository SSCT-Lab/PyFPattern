def compare_rules(connection, module, current_listeners, listener):
    '\n    Compare rules and return rules to add, rules to modify and rules to remove\n    Rules are compared based on priority\n\n    :param connection: ELBv2 boto3 connection\n    :param module: Ansible module object\n    :param current_listeners: list of listeners currently associated with the ELB\n    :param listener: dict object of a listener passed by the user\n    :return:\n    '
    for current_listener in current_listeners:
        if (current_listener['Port'] == listener['Port']):
            listener['ListenerArn'] = current_listener['ListenerArn']
            break
    if ('ListenerArn' in listener):
        current_rules = get_listener_rules(connection, module, listener['ListenerArn'])
    else:
        current_rules = []
    rules_to_modify = []
    rules_to_delete = []
    for current_rule in current_rules:
        current_rule_passed_to_module = False
        for new_rule in listener['Rules'][:]:
            if (current_rule['Priority'] == new_rule['Priority']):
                current_rule_passed_to_module = True
                listener['Rules'].remove(new_rule)
                modified_rule = compare_rule(current_rule, new_rule)
                if modified_rule:
                    modified_rule['Priority'] = int(current_rule['Priority'])
                    modified_rule['RuleArn'] = current_rule['RuleArn']
                    modified_rule['Actions'] = new_rule['Actions']
                    modified_rule['Conditions'] = new_rule['Conditions']
                    rules_to_modify.append(modified_rule)
                break
        if ((not current_rule_passed_to_module) and (not current_rule['IsDefault'])):
            rules_to_delete.append(current_rule['RuleArn'])
    rules_to_add = listener['Rules']
    return (rules_to_add, rules_to_modify, rules_to_delete)