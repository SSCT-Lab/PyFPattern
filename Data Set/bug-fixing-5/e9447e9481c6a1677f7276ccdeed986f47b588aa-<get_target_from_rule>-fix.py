def get_target_from_rule(module, ec2, rule, name, group, groups, vpc_id):
    '\n    Returns tuple of (group_id, ip) after validating rule params.\n\n    rule: Dict describing a rule.\n    name: Name of the security group being managed.\n    groups: Dict of all available security groups.\n\n    AWS accepts an ip range or a security group as target of a rule. This\n    function validate the rule specification and return either a non-None\n    group_id or a non-None ip range.\n    '
    FOREIGN_SECURITY_GROUP_REGEX = '^(\\S+)/(sg-\\S+)/(\\S+)'
    group_id = None
    group_name = None
    ip = None
    target_group_created = False
    if (('group_id' in rule) and ('cidr_ip' in rule)):
        module.fail_json(msg='Specify group_id OR cidr_ip, not both')
    elif (('group_name' in rule) and ('cidr_ip' in rule)):
        module.fail_json(msg='Specify group_name OR cidr_ip, not both')
    elif (('group_id' in rule) and ('group_name' in rule)):
        module.fail_json(msg='Specify group_id OR group_name, not both')
    elif (rule.get('group_id') and re.match(FOREIGN_SECURITY_GROUP_REGEX, rule['group_id'])):
        (owner_id, group_id, group_name) = re.match(FOREIGN_SECURITY_GROUP_REGEX, rule['group_id']).groups()
        group_instance = SecurityGroup(owner_id=owner_id, name=group_name, id=group_id)
        groups[group_id] = group_instance
        groups[group_name] = group_instance
    elif ('group_id' in rule):
        group_id = rule['group_id']
    elif ('group_name' in rule):
        group_name = rule['group_name']
        if (group_name == name):
            group_id = group.id
            groups[group_id] = group
            groups[group_name] = group
        elif ((group_name in groups) and ((vpc_id is None) or (groups[group_name].vpc_id == vpc_id))):
            group_id = groups[group_name].id
        else:
            if (not rule.get('group_desc', '').strip()):
                module.fail_json(msg=('group %s will be automatically created by rule %s and no description was provided' % (group_name, rule)))
            if (not module.check_mode):
                auto_group = ec2.create_security_group(group_name, rule['group_desc'], vpc_id=vpc_id)
                group_id = auto_group.id
                groups[group_id] = auto_group
                groups[group_name] = auto_group
            target_group_created = True
    elif ('cidr_ip' in rule):
        ip = rule['cidr_ip']
    return (group_id, ip, target_group_created)