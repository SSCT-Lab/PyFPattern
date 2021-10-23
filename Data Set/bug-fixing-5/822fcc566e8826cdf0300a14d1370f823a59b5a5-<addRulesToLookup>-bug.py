def addRulesToLookup(rules, prefix, dict):
    for rule in rules:
        for grant in rule.grants:
            dict[make_rule_key(prefix, rule, grant.group_id, grant.cidr_ip)] = (rule, grant)