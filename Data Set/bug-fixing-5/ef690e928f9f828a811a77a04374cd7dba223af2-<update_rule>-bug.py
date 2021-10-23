def update_rule(self, rule_type, rule_control, rule_path, new_type=None, new_control=None, new_path=None, new_args=None):
    rules_to_find = self.get(rule_type, rule_control, rule_path)
    for current_rule in rules_to_find:
        if new_type:
            current_rule.rule_type = new_type
        if new_control:
            current_rule.rule_control = new_control
        if new_path:
            current_rule.rule_path = new_path
        if new_args:
            if isinstance(new_args, str):
                new_args = new_args.replace(' = ', '=')
                new_args = new_args.split(' ')
            current_rule.rule_args = new_args
    return len(rules_to_find)