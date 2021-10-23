

def main():
    argument_spec = dict(name=dict(), group_id=dict(), description=dict(), vpc_id=dict(), rules=dict(type='list'), rules_egress=dict(type='list'), state=dict(default='present', type='str', choices=['present', 'absent']), purge_rules=dict(default=True, required=False, type='bool'), purge_rules_egress=dict(default=True, required=False, type='bool'), tags=dict(required=False, type='dict', aliases=['resource_tags']), purge_tags=dict(default=True, required=False, type='bool'))
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True, required_one_of=[['name', 'group_id']], required_if=[['state', 'present', ['name']]])
    name = module.params['name']
    group_id = module.params['group_id']
    description = module.params['description']
    vpc_id = module.params['vpc_id']
    rules = flatten_nested_targets(module, deepcopy(module.params['rules']))
    rules_egress = flatten_nested_targets(module, deepcopy(module.params['rules_egress']))
    rules = deduplicate_rules_args(rules_expand_sources(rules_expand_ports(rules)))
    rules_egress = deduplicate_rules_args(rules_expand_sources(rules_expand_ports(rules_egress)))
    state = module.params.get('state')
    purge_rules = module.params['purge_rules']
    purge_rules_egress = module.params['purge_rules_egress']
    tags = module.params['tags']
    purge_tags = module.params['purge_tags']
    if ((state == 'present') and (not description)):
        module.fail_json(msg='Must provide description when state is present.')
    changed = False
    client = module.client('ec2')
    verify_rules_with_descriptions_permitted(client, module, rules, rules_egress)
    (group, groups) = group_exists(client, module, vpc_id, group_id, name)
    group_created_new = (not bool(group))
    global current_account_id
    current_account_id = get_aws_account_id(module)
    before = {
        
    }
    after = {
        
    }
    if (state == 'absent'):
        if group:
            before = camel_dict_to_snake_dict(group, ignore_list=['Tags'])
            before['tags'] = boto3_tag_list_to_ansible_dict(before.get('tags', []))
            try:
                if (not module.check_mode):
                    client.delete_security_group(GroupId=group['GroupId'])
            except (BotoCoreError, ClientError) as e:
                module.fail_json_aws(e, msg=("Unable to delete security group '%s'" % group))
            else:
                group = None
                changed = True
        else:
            pass
    elif (state == 'present'):
        if group:
            before = camel_dict_to_snake_dict(group, ignore_list=['Tags'])
            before['tags'] = boto3_tag_list_to_ansible_dict(before.get('tags', []))
            if (group['Description'] != description):
                module.warn('Group description does not match existing group. Descriptions cannot be changed without deleting and re-creating the security group. Try using state=absent to delete, then rerunning this task.')
        else:
            group = create_security_group(client, module, name, description, vpc_id)
            changed = True
        if ((tags is not None) and (group is not None)):
            current_tags = boto3_tag_list_to_ansible_dict(group.get('Tags', []))
            changed |= update_tags(client, module, group['GroupId'], current_tags, tags, purge_tags)
    if group:
        named_tuple_ingress_list = []
        named_tuple_egress_list = []
        current_ingress = sum([list(rule_from_group_permission(p)) for p in group['IpPermissions']], [])
        current_egress = sum([list(rule_from_group_permission(p)) for p in group['IpPermissionsEgress']], [])
        for (new_rules, rule_type, named_tuple_rule_list) in [(rules, 'in', named_tuple_ingress_list), (rules_egress, 'out', named_tuple_egress_list)]:
            if (new_rules is None):
                continue
            for rule in new_rules:
                (target_type, target, target_group_created) = get_target_from_rule(module, client, rule, name, group, groups, vpc_id)
                changed |= target_group_created
                if (rule.get('proto', 'tcp') in ('all', '-1', (- 1))):
                    rule['proto'] = '-1'
                    rule['from_port'] = None
                    rule['to_port'] = None
                try:
                    int(rule.get('proto', 'tcp'))
                    rule['proto'] = to_text(rule.get('proto', 'tcp'))
                    rule['from_port'] = None
                    rule['to_port'] = None
                except ValueError:
                    pass
                named_tuple_rule_list.append(Rule(port_range=(rule['from_port'], rule['to_port']), protocol=to_text(rule.get('proto', 'tcp')), target=target, target_type=target_type, description=rule.get('rule_desc')))
        new_ingress_permissions = [to_permission(r) for r in (set(named_tuple_ingress_list) - set(current_ingress))]
        new_egress_permissions = [to_permission(r) for r in (set(named_tuple_egress_list) - set(current_egress))]
        if ((module.params.get('rules_egress') is None) and ('VpcId' in group)):
            rule = Rule((None, None), '-1', '0.0.0.0/0', 'ipv4', None)
            if (rule in current_egress):
                named_tuple_egress_list.append(rule)
            if (rule not in current_egress):
                current_egress.append(rule)
        present_ingress = list(set(named_tuple_ingress_list).union(set(current_ingress)))
        present_egress = list(set(named_tuple_egress_list).union(set(current_egress)))
        if purge_rules:
            revoke_ingress = []
            for p in present_ingress:
                if (not any([rule_cmp(p, b) for b in named_tuple_ingress_list])):
                    revoke_ingress.append(to_permission(p))
        else:
            revoke_ingress = []
        if (purge_rules_egress and (module.params.get('rules_egress') is not None)):
            if (module.params.get('rules_egress') is []):
                revoke_egress = [to_permission(r) for r in (set(present_egress) - set(named_tuple_egress_list)) if (r != Rule((None, None), '-1', '0.0.0.0/0', 'ipv4', None))]
            else:
                revoke_egress = []
                for p in present_egress:
                    if (not any([rule_cmp(p, b) for b in named_tuple_egress_list])):
                        revoke_egress.append(to_permission(p))
        else:
            revoke_egress = []
        desired_ingress = deepcopy(named_tuple_ingress_list)
        desired_egress = deepcopy(named_tuple_egress_list)
        changed |= update_rule_descriptions(module, group['GroupId'], present_ingress, named_tuple_ingress_list, present_egress, named_tuple_egress_list)
        changed |= remove_old_permissions(client, module, revoke_ingress, revoke_egress, group['GroupId'])
        rule_msg = 'Revoking {0}, and egress {1}'.format(revoke_ingress, revoke_egress)
        new_ingress_permissions = [to_permission(r) for r in (set(named_tuple_ingress_list) - set(current_ingress))]
        new_ingress_permissions = rules_to_permissions((set(named_tuple_ingress_list) - set(current_ingress)))
        new_egress_permissions = rules_to_permissions((set(named_tuple_egress_list) - set(current_egress)))
        changed |= add_new_permissions(client, module, new_ingress_permissions, new_egress_permissions, group['GroupId'])
        if (group_created_new and (module.params.get('rules') is None) and (module.params.get('rules_egress') is None)):
            security_group = get_security_groups_with_backoff(client, GroupIds=[group['GroupId']])['SecurityGroups'][0]
        elif (changed and (not module.check_mode)):
            security_group = wait_for_rule_propagation(module, group, desired_ingress, desired_egress, purge_rules, purge_rules_egress)
        else:
            security_group = get_security_groups_with_backoff(client, GroupIds=[group['GroupId']])['SecurityGroups'][0]
        security_group = camel_dict_to_snake_dict(security_group, ignore_list=['Tags'])
        security_group['tags'] = boto3_tag_list_to_ansible_dict(security_group.get('tags', []))
    else:
        security_group = {
            'group_id': None,
        }
    if module._diff:
        if (module.params['state'] == 'present'):
            after = get_diff_final_resource(client, module, security_group)
        security_group['diff'] = [{
            'before': before,
            'after': after,
        }]
    module.exit_json(changed=changed, **security_group)
