def add_module_arguments(self, rule_type, rule_control, rule_path, args_to_add):
    rules_to_find = self.get(rule_type, rule_control, rule_path)
    args_to_add = parse_module_arguments(args_to_add)
    changes = 0
    for current_rule in rules_to_find:
        rule_changed = False
        simple_new_args = set()
        key_value_new_args = dict()
        for arg in args_to_add:
            if arg.startswith('['):
                continue
            elif ('=' in arg):
                (key, value) = arg.split('=')
                key_value_new_args[key] = value
            else:
                simple_new_args.add(arg)
        key_value_new_args_set = set(key_value_new_args)
        simple_current_args = set()
        key_value_current_args = dict()
        for arg in current_rule.rule_args:
            if arg.startswith('['):
                continue
            elif ('=' in arg):
                (key, value) = arg.split('=')
                key_value_current_args[key] = value
            else:
                simple_current_args.add(arg)
        key_value_current_args_set = set(key_value_current_args)
        new_args_to_add = list()
        if simple_new_args.difference(simple_current_args):
            for arg in simple_new_args.difference(simple_current_args):
                new_args_to_add.append(arg)
        if key_value_new_args_set.difference(key_value_current_args_set):
            for key in key_value_new_args_set.difference(key_value_current_args_set):
                new_args_to_add.append(((key + '=') + key_value_new_args[key]))
        if new_args_to_add:
            current_rule.rule_args += new_args_to_add
            rule_changed = True
        if key_value_new_args_set.intersection(key_value_current_args_set):
            for key in key_value_new_args_set.intersection(key_value_current_args_set):
                if (key_value_current_args[key] != key_value_new_args[key]):
                    arg_index = current_rule.rule_args.index(((key + '=') + key_value_current_args[key]))
                    current_rule.rule_args[arg_index] = str(((key + '=') + key_value_new_args[key]))
                    rule_changed = True
        if rule_changed:
            changes += 1
    return changes