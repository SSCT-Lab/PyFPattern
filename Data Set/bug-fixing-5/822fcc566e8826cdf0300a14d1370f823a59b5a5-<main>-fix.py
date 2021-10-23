def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(name=dict(type='str', required=True), description=dict(type='str', required=False), vpc_id=dict(type='str'), rules=dict(type='list'), rules_egress=dict(type='list'), state=dict(default='present', type='str', choices=['present', 'absent']), purge_rules=dict(default=True, required=False, type='bool'), purge_rules_egress=dict(default=True, required=False, type='bool')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    name = module.params['name']
    description = module.params['description']
    vpc_id = module.params['vpc_id']
    rules = deduplicate_rules_args(rules_expand_sources(rules_expand_ports(module.params['rules'])))
    rules_egress = deduplicate_rules_args(rules_expand_sources(rules_expand_ports(module.params['rules_egress'])))
    state = module.params.get('state')
    purge_rules = module.params['purge_rules']
    purge_rules_egress = module.params['purge_rules_egress']
    if ((state == 'present') and (not description)):
        module.fail_json(msg='Must provide description when state is present.')
    changed = False
    ec2 = ec2_connect(module)
    group = None
    groups = {
        
    }
    try:
        security_groups = ec2.get_all_security_groups()
    except BotoServerError as e:
        module.fail_json(msg=('Error in get_all_security_groups: %s' % e.message), exception=traceback.format_exc())
    for curGroup in security_groups:
        groups[curGroup.id] = curGroup
        if (curGroup.name in groups):
            if ((vpc_id is None) or (curGroup.vpc_id == vpc_id)):
                groups[curGroup.name] = curGroup
        else:
            groups[curGroup.name] = curGroup
        if ((curGroup.name == name) and ((vpc_id is None) or (curGroup.vpc_id == vpc_id))):
            group = curGroup
    if (state == 'absent'):
        if group:
            try:
                if (not module.check_mode):
                    group.delete()
            except BotoServerError as e:
                module.fail_json(msg=("Unable to delete security group '%s' - %s" % (group, e.message)), exception=traceback.format_exc())
            else:
                group = None
                changed = True
        else:
            pass
    elif (state == 'present'):
        if group:
            if (group.description != description):
                module.fail_json(msg='Group description does not match existing group. ec2_group does not support this case.')
        else:
            if (not module.check_mode):
                group = ec2.create_security_group(name, description, vpc_id=vpc_id)
                while (len(ec2.get_all_security_groups(filters={
                    'group_id': group.id,
                })) == 0):
                    time.sleep(0.1)
                group = ec2.get_all_security_groups(group_ids=(group.id,))[0]
            changed = True
    else:
        module.fail_json(msg=('Unsupported state requested: %s' % state))
    if group:
        groupRules = {
            
        }
        addRulesToLookup(group.rules, 'in', groupRules)
        if (rules is not None):
            for rule in rules:
                validate_rule(module, rule)
                (group_id, ip, target_group_created) = get_target_from_rule(module, ec2, rule, name, group, groups, vpc_id)
                if target_group_created:
                    changed = True
                if (rule['proto'] in ('all', '-1', (- 1))):
                    rule['proto'] = (- 1)
                    rule['from_port'] = None
                    rule['to_port'] = None
                if (not isinstance(ip, list)):
                    ip = [ip]
                for thisip in ip:
                    ruleId = make_rule_key('in', rule, group_id, thisip)
                    if (ruleId not in groupRules):
                        grantGroup = None
                        if group_id:
                            grantGroup = groups[group_id]
                        if (not module.check_mode):
                            group.authorize(rule['proto'], rule['from_port'], rule['to_port'], thisip, grantGroup)
                        changed = True
                    else:
                        del groupRules[ruleId]
        if purge_rules:
            for (rule, grant) in groupRules.values():
                grantGroup = None
                if grant.group_id:
                    if (grant.owner_id != group.owner_id):
                        group_instance = SecurityGroup(owner_id=grant.owner_id, name=grant.name, id=grant.group_id)
                        groups[grant.group_id] = group_instance
                        groups[grant.name] = group_instance
                    grantGroup = groups[grant.group_id]
                if (not module.check_mode):
                    group.revoke(rule.ip_protocol, rule.from_port, rule.to_port, grant.cidr_ip, grantGroup)
                changed = True
        groupRules = {
            
        }
        addRulesToLookup(group.rules_egress, 'out', groupRules)
        if (rules_egress is not None):
            for rule in rules_egress:
                validate_rule(module, rule)
                (group_id, ip, target_group_created) = get_target_from_rule(module, ec2, rule, name, group, groups, vpc_id)
                if target_group_created:
                    changed = True
                if (rule['proto'] in ('all', '-1', (- 1))):
                    rule['proto'] = (- 1)
                    rule['from_port'] = None
                    rule['to_port'] = None
                if (not isinstance(ip, list)):
                    ip = [ip]
                for thisip in ip:
                    ruleId = make_rule_key('out', rule, group_id, thisip)
                    if (ruleId in groupRules):
                        del groupRules[ruleId]
                    else:
                        grantGroup = None
                        if group_id:
                            grantGroup = groups[group_id].id
                        if (not module.check_mode):
                            ec2.authorize_security_group_egress(group_id=group.id, ip_protocol=rule['proto'], from_port=rule['from_port'], to_port=rule['to_port'], src_group_id=grantGroup, cidr_ip=thisip)
                        changed = True
        else:
            default_egress_rule = 'out--1-None-None-None-0.0.0.0/0'
            if (default_egress_rule not in groupRules):
                if (not module.check_mode):
                    ec2.authorize_security_group_egress(group_id=group.id, ip_protocol=(- 1), from_port=None, to_port=None, src_group_id=None, cidr_ip='0.0.0.0/0')
                changed = True
            else:
                del groupRules[default_egress_rule]
        if purge_rules_egress:
            for (rule, grant) in groupRules.values():
                grantGroup = None
                if grant.group_id:
                    grantGroup = groups[grant.group_id].id
                if (not module.check_mode):
                    ec2.revoke_security_group_egress(group_id=group.id, ip_protocol=rule.ip_protocol, from_port=rule.from_port, to_port=rule.to_port, src_group_id=grantGroup, cidr_ip=grant.cidr_ip)
                changed = True
    if group:
        module.exit_json(changed=changed, group_id=group.id)
    else:
        module.exit_json(changed=changed, group_id=None)