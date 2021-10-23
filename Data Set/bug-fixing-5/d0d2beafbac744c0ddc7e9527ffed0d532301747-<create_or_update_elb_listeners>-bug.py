def create_or_update_elb_listeners(connection, module, elb):
    'Create or update ELB listeners. Return true if changed, else false'
    listener_changed = False
    listeners = module.params.get('listeners')
    listeners_rules = deepcopy(listeners)
    listener_matches = False
    if (listeners is not None):
        current_listeners = get_elb_listeners(connection, module, elb['LoadBalancerArn'])
        current_listeners_array = []
        if current_listeners:
            for current_listener in current_listeners:
                del current_listener['ListenerArn']
                del current_listener['LoadBalancerArn']
                current_listeners_s = convert(current_listener)
                current_listeners_array.append(current_listeners_s)
            for curr_listener in current_listeners_array:
                for default_action in curr_listener['DefaultActions']:
                    default_action['TargetGroupName'] = convert_tg_arn_name(connection, module, default_action['TargetGroupArn'])
                    del default_action['TargetGroupArn']
            listeners_to_add = []
            for listener in listeners:
                if ('Rules' in listener.keys()):
                    del listener['Rules']
            for listener in listeners:
                if (listener not in current_listeners_array):
                    listeners_to_add.append(listener)
            listeners_to_remove = []
            for current_listener in current_listeners_array:
                if (current_listener not in listeners):
                    listeners_to_remove.append(current_listener)
            if listeners_to_remove:
                arns_to_remove = []
                current_listeners = connection.describe_listeners(LoadBalancerArn=elb['LoadBalancerArn'])['Listeners']
                listener_changed = True
                for listener in listeners_to_remove:
                    for current_listener in current_listeners:
                        if (current_listener['Port'] == listener['Port']):
                            arns_to_remove.append(current_listener['ListenerArn'])
                for arn in arns_to_remove:
                    connection.delete_listener(ListenerArn=arn)
            if listeners_to_add:
                listener_changed = True
                for listener in listeners_to_add:
                    listener['LoadBalancerArn'] = elb['LoadBalancerArn']
                    for default_action in listener['DefaultActions']:
                        default_action['TargetGroupArn'] = convert_tg_name_arn(connection, module, default_action['TargetGroupName'])
                        del default_action['TargetGroupName']
                    connection.create_listener(**listener)
            current_listeners = connection.describe_listeners(LoadBalancerArn=elb['LoadBalancerArn'])['Listeners']
            for listener in listeners_rules:
                if ('Rules' in listener.keys()):
                    for current_listener in current_listeners:
                        if (current_listener['Port'] == listener['Port']):
                            current_rules = connection.describe_rules(ListenerArn=current_listener['ListenerArn'])['Rules']
                            current_rules_array = []
                            for rules in current_rules:
                                del rules['RuleArn']
                                del rules['IsDefault']
                                if (rules['Priority'] != 'default'):
                                    current_rules_s = convert(rules)
                                    current_rules_array.append(current_rules_s)
                            for curr_rule in current_rules_array:
                                for action in curr_rule['Actions']:
                                    action['TargetGroupName'] = convert_tg_arn_name(connection, module, action['TargetGroupArn'])
                                    del action['TargetGroupArn']
                            rules_to_remove = []
                            for current_rule in current_rules_array:
                                if listener['Rules']:
                                    if (current_rule not in listener['Rules']):
                                        rules_to_remove.append(current_rule)
                                else:
                                    rules_to_remove.append(current_rule)
                            if rules_to_remove:
                                rule_arns_to_remove = []
                                current_rules = connection.describe_rules(ListenerArn=current_listener['ListenerArn'])['Rules']
                                for rules in rules_to_remove:
                                    for current_rule in current_rules:
                                        if ((current_rule['Conditions'] == rules['Conditions']) and (current_rule['Priority'] == rules['Priority'])):
                                            rule_arns_to_remove.append(current_rule['RuleArn'])
                                listener_changed = True
                                for arn in rule_arns_to_remove:
                                    connection.delete_rule(RuleArn=arn)
                            rules_to_add = []
                            if listener['Rules']:
                                for rules in listener['Rules']:
                                    if (rules not in current_rules_array):
                                        rules_to_add.append(rules)
                            if rules_to_add:
                                listener_changed = True
                                for rule in rules_to_add:
                                    rule['ListenerArn'] = current_listener['ListenerArn']
                                    rule['Priority'] = int(rule['Priority'])
                                    for action in rule['Actions']:
                                        action['TargetGroupArn'] = convert_tg_name_arn(connection, module, action['TargetGroupName'])
                                        del action['TargetGroupName']
                                    connection.create_rule(**rule)
        else:
            for listener in listeners:
                listener['LoadBalancerArn'] = elb['LoadBalancerArn']
                if ('Rules' in listener.keys()):
                    del listener['Rules']
                for default_action in listener['DefaultActions']:
                    default_action['TargetGroupArn'] = convert_tg_name_arn(connection, module, default_action['TargetGroupName'])
                    del default_action['TargetGroupName']
                connection.create_listener(**listener)
                listener_changed = True
            current_listeners = connection.describe_listeners(LoadBalancerArn=elb['LoadBalancerArn'])['Listeners']
            for current_listener in current_listeners:
                for listener in listeners_rules:
                    if (current_listener['Port'] == listener['Port']):
                        if ('Rules' in listener.keys()):
                            for rules in listener['Rules']:
                                rules['ListenerArn'] = current_listener['ListenerArn']
                                rules['Priority'] = int(rules['Priority'])
                                for action in rules['Actions']:
                                    action['TargetGroupArn'] = convert_tg_name_arn(connection, module, action['TargetGroupName'])
                                    del action['TargetGroupName']
                                connection.create_rule(**rules)
    else:
        current_listeners = connection.describe_listeners(LoadBalancerArn=elb['LoadBalancerArn'])['Listeners']
        if current_listeners:
            for listener in current_listeners:
                listener_changed = True
                connection.delete_listener(ListenerArn=listener['ListenerArn'])
    return listener_changed