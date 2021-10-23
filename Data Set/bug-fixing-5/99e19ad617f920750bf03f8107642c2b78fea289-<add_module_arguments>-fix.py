def add_module_arguments(service, old_rule, module_args):
    result = {
        'action': 'args_present',
    }
    changed = False
    change_count = 0
    if isinstance(module_args, ansible.module_utils.six.string_types):
        module_args = module_args.split(' ')
    for rule in service.rules:
        if ((old_rule.rule_type == rule.rule_type) and (old_rule.rule_control == rule.rule_control) and (old_rule.rule_module_path == rule.rule_module_path)):
            for arg_to_add in module_args:
                if ('=' in arg_to_add):
                    pre_string = arg_to_add[:(arg_to_add.index('=') + 1)]
                    indicies = [i for (i, arg) in enumerate(rule.rule_module_args) if arg.startswith(pre_string)]
                    for i in indicies:
                        if (rule.rule_module_args[i] != arg_to_add):
                            rule.rule_module_args[i] = arg_to_add
                            changed = True
                            result[('updated_arg_' + str(change_count))] = arg_to_add
                            result[('in_rule_' + str(change_count))] = str(rule)
                            change_count += 1
                elif (arg_to_add not in rule.rule_module_args):
                    rule.rule_module_args.append(arg_to_add)
                    changed = True
                    result[('added_arg_' + str(change_count))] = arg_to_add
                    result[('to_rule_' + str(change_count))] = str(rule)
                    change_count += 1
    result['change_count'] = change_count
    return (changed, result)