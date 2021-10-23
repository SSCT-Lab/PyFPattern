@classmethod
def rule_from_string(cls, line):
    match = RULE_REGEX.search(line)
    return cls(match.group('rule_type'), match.group('control'), match.group('path'), match.group('args'))