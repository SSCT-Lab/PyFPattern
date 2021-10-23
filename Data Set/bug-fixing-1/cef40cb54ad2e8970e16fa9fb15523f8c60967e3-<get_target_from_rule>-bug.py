

def get_target_from_rule(module, client, rule, name, group, groups, vpc_id):
    '\n    Returns tuple of (group_id, ip) after validating rule params.\n\n    rule: Dict describing a rule.\n    name: Name of the security group being managed.\n    groups: Dict of all available security groups.\n\n    AWS accepts an ip range or a security group as target of a rule. This\n    function validate the rule specification and return either a non-None\n    group_id or a non-None ip range.\n    '
    FOREIGN_SECURITY_GROUP_REGEX = '^(\\S+)/(sg-\\S+)/(\\S+)'
    group_id = None
    group_name = None
    ip = None
    ipv6 = None
    target_group_created = False
    if (('group_id' in rule) and ('cidr_ip' in rule)):
        module.fail_json(msg='Specify group_id OR cidr_ip, not both')
    elif (('group_name' in rule) and ('cidr_ip' in rule)):
        module.fail_json(msg='Specify group_name OR cidr_ip, not both')
    elif (('group_id' in rule) and ('cidr_ipv6' in rule)):
        module.fail_json(msg='Specify group_id OR cidr_ipv6, not both')
    elif (('group_name' in rule) and ('cidr_ipv6' in rule)):
        module.fail_json(msg='Specify group_name OR cidr_ipv6, not both')
    elif (('group_id' in rule) and ('group_name' in rule)):
        module.fail_json(msg='Specify group_id OR group_name, not both')
    elif (('cidr_ip' in rule) and ('cidr_ipv6' in rule)):
        module.fail_json(msg='Specify cidr_ip OR cidr_ipv6, not both')
    elif (rule.get('group_id') and re.match(FOREIGN_SECURITY_GROUP_REGEX, rule['group_id'])):
        (owner_id, group_id, group_name) = re.match(FOREIGN_SECURITY_GROUP_REGEX, rule['group_id']).groups()
        group_instance = dict(GroupId=group_id, GroupName=group_name)
        groups[group_id] = group_instance
        groups[group_name] = group_instance
    elif ('group_id' in rule):
        group_id = rule['group_id']
    elif ('group_name' in rule):
        group_name = rule['group_name']
        if (group_name == name):
            group_id = group['GroupId']
            groups[group_id] = group
            groups[group_name] = group
        elif ((group_name in groups) and ((vpc_id is None) or (groups[group_name]['VpcId'] == vpc_id))):
            group_id = groups[group_name]['GroupId']
        else:
            if (not rule.get('group_desc', '').strip()):
                module.fail_json(msg=('group %s will be automatically created by rule %s and no description was provided' % (group_name, rule)))
            if (not module.check_mode):
                params = dict(GroupName=group_name, Description=rule['group_desc'])
                if vpc_id:
                    params['VpcId'] = vpc_id
                auto_group = client.create_security_group(**params)
                group_id = auto_group['GroupId']
                groups[group_id] = auto_group
                groups[group_name] = auto_group
            target_group_created = True
    elif ('cidr_ip' in rule):
        ip = rule['cidr_ip']
    elif ('cidr_ipv6' in rule):
        ipv6 = rule['cidr_ipv6']
    return (group_id, ip, ipv6, target_group_created)
