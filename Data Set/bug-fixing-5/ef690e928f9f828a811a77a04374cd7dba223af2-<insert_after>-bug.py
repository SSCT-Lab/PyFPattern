def insert_after(self, rule_type, rule_control, rule_path, new_type=None, new_control=None, new_path=None, new_args=None):
    rules_to_find = self.get(rule_type, rule_control, rule_path)
    changed = 0
    for current_rule in rules_to_find:
        next_rule = current_rule.next
        while ((next_rule is not None) and isinstance(next_rule, PamdComment)):
            next_rule = next_rule.next
        new_rule = PamdRule(new_type, new_control, new_path, new_args)
        if ((next_rule is not None) and (not next_rule.matches(new_type, new_control, new_path))):
            next_rule.prev = new_rule
            new_rule.next = next_rule
            new_rule.prev = current_rule
            current_rule.next = new_rule
            changed += 1
        elif (next_rule is None):
            new_rule.prev = self._tail
            new_rule.next = None
            self._tail.next = new_rule
            self._tail = new_rule
            current_rule.next = new_rule
            changed += 1
    return changed