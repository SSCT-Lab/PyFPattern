def addRulesToLookup(rules, prefix, rules_dict):
    for rule in rules:
        for grant in rule.grants:
            rules_dict[make_rule_key(prefix, rule, grant.group_id, grant.cidr_ip)] = (rule, grant)