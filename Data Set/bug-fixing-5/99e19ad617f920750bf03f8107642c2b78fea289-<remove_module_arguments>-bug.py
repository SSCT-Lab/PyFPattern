def remove_module_arguments(service, old_rule, module_args):
    result = {
        'action': 'args_absent',
    }
    changed = False
    change_count = 0
    for rule in service.rules:
        if ((old_rule.rule_type == rule.rule_type) and (old_rule.rule_control == rule.rule_control) and (old_rule.rule_module_path == rule.rule_module_path)):
            for arg_to_remove in module_args.split():
                for arg in rule.rule_module_args:
                    if (arg == arg_to_remove):
                        rule.rule_module_args.remove(arg)
                        changed = True
                        result[('removed_arg_' + str(change_count))] = arg
                        result[('from_rule_' + str(change_count))] = str(rule)
                        change_count += 1
    result['change_count'] = change_count
    return (changed, result)