@classmethod
def rule_from_string(cls, line):
    rule_match = RULE_REGEX.search(line)
    rule_args = parse_module_arguments(rule_match.group('args'))
    return cls(rule_match.group('rule_type'), rule_match.group('control'), rule_match.group('path'), rule_args)