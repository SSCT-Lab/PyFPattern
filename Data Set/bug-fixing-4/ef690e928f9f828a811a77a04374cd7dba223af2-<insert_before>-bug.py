def insert_before(self, rule_type, rule_control, rule_path, new_type=None, new_control=None, new_path=None, new_args=None):
    rules_to_find = self.get(rule_type, rule_control, rule_path)
    changed = 0
    for current_rule in rules_to_find:
        new_rule = PamdRule(new_type, new_control, new_path, new_args)
        previous_rule = current_rule.prev
        while ((previous_rule is not None) and isinstance(previous_rule, PamdComment)):
            previous_rule = previous_rule.prev
        if ((previous_rule is not None) and (not previous_rule.matches(new_type, new_control, new_path))):
            previous_rule.next = new_rule
            new_rule.prev = previous_rule
            new_rule.next = current_rule
            current_rule.prev = new_rule
            changed += 1
        elif (previous_rule is None):
            if (current_rule.prev is None):
                self._head = new_rule
            else:
                current_rule.prev.next = new_rule
            new_rule.prev = current_rule.prev
            new_rule.next = current_rule
            current_rule.prev = new_rule
            changed += 1
    return changed