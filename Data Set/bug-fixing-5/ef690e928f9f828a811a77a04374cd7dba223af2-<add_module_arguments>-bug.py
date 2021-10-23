def add_module_arguments(self, rule_type, rule_control, rule_path, args_to_add):
    rules_to_find = self.get(rule_type, rule_control, rule_path)
    changed = 0
    for current_rule in rules_to_find:
        if isinstance(args_to_add, str):
            args_to_add = args_to_add.replace(' = ', '=')
            args_to_add = args_to_add.split(' ')
        if (not args_to_add):
            args_to_add = []
        new_args = [arg for arg in args_to_add if (arg not in current_rule.rule_args)]
        if (not new_args):
            continue
        current_rule.rule_args = (current_rule.rule_args + new_args)
        changed += 1
    return changed