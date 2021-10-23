def update_rule(self, rule_type, rule_control, rule_path, new_type=None, new_control=None, new_path=None, new_args=None):
    rules_to_find = self.get(rule_type, rule_control, rule_path)
    new_args = parse_module_arguments(new_args)
    changes = 0
    for current_rule in rules_to_find:
        rule_changed = False
        if new_type:
            if (current_rule.rule_type != new_type):
                rule_changed = True
                current_rule.rule_type = new_type
        if new_control:
            if (current_rule.rule_control != new_control):
                rule_changed = True
                current_rule.rule_control = new_control
        if new_path:
            if (current_rule.rule_path != new_path):
                rule_changed = True
                current_rule.rule_path = new_path
        if new_args:
            if (current_rule.rule_args != new_args):
                rule_changed = True
                current_rule.rule_args = new_args
        if rule_changed:
            changes += 1
    return changes