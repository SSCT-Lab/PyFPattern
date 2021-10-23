def insert_after_rule(service, old_rule, new_rule):
    index = 0
    change_count = 0
    result = {
        'action': 'insert_after_rule',
    }
    changed = False
    for rule in service.rules:
        if ((old_rule.rule_type == rule.rule_type) and (old_rule.rule_control == rule.rule_control) and (old_rule.rule_module_path == rule.rule_module_path)):
            if ((new_rule.rule_type != service.rules[(index + 1)].rule_type) or (new_rule.rule_control != service.rules[(index + 1)].rule_control) or (new_rule.rule_module_path != service.rules[(index + 1)].rule_module_path)):
                service.rules.insert((index + 1), new_rule)
                changed = True
            if changed:
                result['new_rule'] = str(new_rule)
                result[('after_rule_' + str(change_count))] = str(rule)
                change_count += 1
        index += 1
    result['change_count'] = change_count
    return (changed, result)