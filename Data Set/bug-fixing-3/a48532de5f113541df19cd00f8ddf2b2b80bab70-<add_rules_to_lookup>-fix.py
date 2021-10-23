def add_rules_to_lookup(ipPermissions, group_id, prefix, dict):
    for rule in ipPermissions:
        for groupGrant in rule.get('UserIdGroupPairs', []):
            dict[make_rule_key(prefix, rule, group_id, groupGrant.get('GroupId'))] = (rule, groupGrant)
        for ipv4Grants in rule.get('IpRanges', []):
            dict[make_rule_key(prefix, rule, group_id, ipv4Grants.get('CidrIp'))] = (rule, ipv4Grants)
        for ipv6Grants in rule.get('Ipv6Ranges', []):
            dict[make_rule_key(prefix, rule, group_id, ipv6Grants.get('CidrIpv6'))] = (rule, ipv6Grants)