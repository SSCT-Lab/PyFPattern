def remove_module_arguments(self, rule_type, rule_control, rule_path, args_to_remove):
    rules_to_find = self.get(rule_type, rule_control, rule_path)
    args_to_remove = parse_module_arguments(args_to_remove)
    changes = 0
    for current_rule in rules_to_find:
        if (not args_to_remove):
            args_to_remove = []
        if (not list((set(current_rule.rule_args) & set(args_to_remove)))):
            continue
        current_rule.rule_args = [arg for arg in current_rule.rule_args if (arg not in args_to_remove)]
        changes += 1
    return changes