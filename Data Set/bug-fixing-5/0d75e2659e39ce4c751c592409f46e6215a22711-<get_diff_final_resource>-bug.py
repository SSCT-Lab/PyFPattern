def get_diff_final_resource(client, module, security_group):

    def get_account_id(security_group, module):
        try:
            owner_id = security_group.get('owner_id', module.client('sts').get_caller_identity()['Account'])
        except (BotoCoreError, ClientError) as e:
            owner_id = 'Unable to determine owner_id: {0}'.format(to_text(e))
        return owner_id

    def get_final_tags(security_group_tags, specified_tags, purge_tags):
        if (specified_tags is None):
            return security_group_tags
        (tags_need_modify, tags_to_delete) = compare_aws_tags(security_group_tags, specified_tags, purge_tags)
        end_result_tags = dict(((k, v) for (k, v) in specified_tags.items() if (k not in tags_to_delete)))
        end_result_tags.update(dict(((k, v) for (k, v) in security_group_tags.items() if (k not in tags_to_delete))))
        end_result_tags.update(tags_need_modify)
        return end_result_tags

    def get_final_rules(client, module, security_group_rules, specified_rules, purge_rules):
        if (specified_rules is None):
            return security_group_rules
        if purge_rules:
            final_rules = []
        else:
            final_rules = list(security_group_rules)
        specified_rules = flatten_nested_targets(module, deepcopy(specified_rules))
        for rule in specified_rules:
            format_rule = {
                'from_port': None,
                'to_port': None,
                'ip_protocol': rule.get('proto', 'tcp'),
                'ip_ranges': [],
                'ipv6_ranges': [],
                'prefix_list_ids': [],
                'user_id_group_pairs': [],
            }
            if (rule.get('proto', 'tcp') in ('all', '-1', (- 1))):
                format_rule['ip_protocol'] = '-1'
                format_rule.pop('from_port')
                format_rule.pop('to_port')
            elif rule.get('ports'):
                if (rule.get('ports') and (isinstance(rule['ports'], string_types) or isinstance(rule['ports'], int))):
                    rule['ports'] = [rule['ports']]
                for port in rule.get('ports'):
                    if (isinstance(port, string_types) and ('-' in port)):
                        (format_rule['from_port'], format_rule['to_port']) = port.split('-')
                    else:
                        format_rule['from_port'] = format_rule['to_port'] = port
            elif (rule.get('from_port') or rule.get('to_port')):
                format_rule['from_port'] = rule.get('from_port', rule.get('to_port'))
                format_rule['to_port'] = rule.get('to_port', rule.get('from_port'))
            for source_type in ('cidr_ip', 'cidr_ipv6', 'prefix_list_id'):
                if rule.get(source_type):
                    rule_key = {
                        'cidr_ip': 'ip_ranges',
                        'cidr_ipv6': 'ipv6_ranges',
                        'prefix_list_id': 'prefix_list_ids',
                    }.get(source_type)
                    if rule.get('rule_desc'):
                        format_rule[rule_key] = [{
                            source_type: rule[source_type],
                            'description': rule['rule_desc'],
                        }]
                    else:
                        if (not isinstance(rule[source_type], list)):
                            rule[source_type] = [rule[source_type]]
                        format_rule[rule_key] = [{
                            source_type: target,
                        } for target in rule[source_type]]
            if (rule.get('group_id') or rule.get('group_name')):
                rule_sg = camel_dict_to_snake_dict(group_exists(client, module, module.params['vpc_id'], rule.get('group_id'), rule.get('group_name'))[0])
                format_rule['user_id_group_pairs'] = [{
                    'description': rule_sg.get('description', rule_sg.get('group_desc')),
                    'group_id': rule_sg.get('group_id', rule.get('group_id')),
                    'group_name': rule_sg.get('group_name', rule.get('group_name')),
                    'peering_status': rule_sg.get('peering_status'),
                    'user_id': rule_sg.get('user_id', get_account_id(security_group, module)),
                    'vpc_id': rule_sg.get('vpc_id', module.params['vpc_id']),
                    'vpc_peering_connection_id': rule_sg.get('vpc_peering_connection_id'),
                }]
                for (k, v) in format_rule['user_id_group_pairs'][0].items():
                    if (v is None):
                        format_rule['user_id_group_pairs'][0].pop(k)
            final_rules.append(format_rule)
            final_rules.sort(key=(lambda x: x.get('cidr_ip', x.get('ip_ranges', x.get('ipv6_ranges', x.get('prefix_list_ids', x.get('user_id_group_pairs')))))))
        return final_rules
    security_group_ingress = security_group.get('ip_permissions', [])
    specified_ingress = module.params['rules']
    purge_ingress = module.params['purge_rules']
    security_group_egress = security_group.get('ip_permissions_egress', [])
    specified_egress = module.params['rules_egress']
    purge_egress = module.params['purge_rules_egress']
    return {
        'description': module.params['description'],
        'group_id': security_group.get('group_id', 'sg-xxxxxxxx'),
        'group_name': security_group.get('group_name', module.params['name']),
        'ip_permissions': get_final_rules(client, module, security_group_ingress, specified_ingress, purge_ingress),
        'ip_permissions_egress': get_final_rules(client, module, security_group_egress, specified_egress, purge_egress),
        'owner_id': get_account_id(security_group, module),
        'tags': get_final_tags(security_group.get('tags', {
            
        }), module.params['tags'], module.params['purge_tags']),
        'vpc_id': security_group.get('vpc_id', module.params['vpc_id']),
    }