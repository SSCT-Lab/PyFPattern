def set_rules(api, name, rules_list):
    updated = False
    if (rules_list is None):
        return False
    rules_list = list(enumerate(rules_list))
    try:
        current_rules = map((lambda x: (x['priority'], x['rule_name'])), get_rules(api, name))
        to_add_rules = []
        for (i, x) in rules_list:
            if ((i, x) not in current_rules):
                to_add_rules.append({
                    'priority': i,
                    'rule_name': x,
                })
        to_del_rules = []
        for (i, x) in current_rules:
            if ((i, x) not in rules_list):
                to_del_rules.append({
                    'priority': i,
                    'rule_name': x,
                })
        if (len(to_del_rules) > 0):
            api.LocalLB.VirtualServer.remove_rule(virtual_servers=[name], rules=[to_del_rules])
            updated = True
        if (len(to_add_rules) > 0):
            api.LocalLB.VirtualServer.add_rule(virtual_servers=[name], rules=[to_add_rules])
            updated = True
        return updated
    except bigsuds.OperationFailed as e:
        raise Exception(('Error on setting rules : %s' % e))