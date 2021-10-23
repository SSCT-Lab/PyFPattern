

def compare_rules(self):
    '\n\n        :return:\n        '
    rules_to_modify = []
    rules_to_delete = []
    rules_to_add = deepcopy(self.rules)
    for current_rule in self.current_rules:
        current_rule_passed_to_module = False
        for new_rule in self.rules[:]:
            if (current_rule['Priority'] == str(new_rule['Priority'])):
                current_rule_passed_to_module = True
                rules_to_add.remove(new_rule)
                modified_rule = self._compare_rule(current_rule, new_rule)
                if modified_rule:
                    modified_rule['Priority'] = int(current_rule['Priority'])
                    modified_rule['RuleArn'] = current_rule['RuleArn']
                    modified_rule['Actions'] = new_rule['Actions']
                    modified_rule['Conditions'] = new_rule['Conditions']
                    rules_to_modify.append(modified_rule)
                break
        if ((not current_rule_passed_to_module) and (not current_rule['IsDefault'])):
            rules_to_delete.append(current_rule['RuleArn'])
    return (rules_to_add, rules_to_modify, rules_to_delete)
