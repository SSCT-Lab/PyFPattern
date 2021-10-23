

def rule_to_string(rule):
    strings = list()
    for (key, value) in rule.items():
        strings.append(('%s=%s' % (key, value)))
    return ', '.join(strings)
