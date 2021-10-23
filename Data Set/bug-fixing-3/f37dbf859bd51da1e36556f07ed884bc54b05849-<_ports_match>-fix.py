def _ports_match(protocol, module_min, module_max, rule_min, rule_max):
    '\n    Capture the complex port matching logic.\n\n    The port values coming in for the module might be -1 (for ICMP),\n    which will work only for Nova, but this is handled by sdk. Likewise,\n    they might be None, which works for Neutron, but not Nova. This too is\n    handled by sdk. Since sdk will consistently return these port\n    values as None, we need to convert any -1 values input to the module\n    to None here for comparison.\n\n    For TCP and UDP protocols, None values for both min and max are\n    represented as the range 1-65535 for Nova, but remain None for\n    Neutron. sdk returns the full range when Nova is the backend (since\n    that is how Nova stores them), and None values for Neutron. If None\n    values are input to the module for both values, then we need to adjust\n    for comparison.\n    '
    if (protocol == 'icmp'):
        if (module_min and (int(module_min) == (- 1))):
            module_min = None
        if (module_max and (int(module_max) == (- 1))):
            module_max = None
    if (protocol == 'any'):
        return True
    if ((protocol in ['tcp', 'udp']) or (protocol is None)):
        if (module_min and module_max and (int(module_min) == int(module_max) == (- 1))):
            module_min = None
            module_max = None
        if (((module_min is None) and (module_max is None)) and (rule_min and (int(rule_min) == 1) and rule_max and (int(rule_max) == 65535))):
            return True
    if module_min:
        module_min = int(module_min)
    if module_max:
        module_max = int(module_max)
    if rule_min:
        rule_min = int(rule_min)
    if rule_max:
        rule_max = int(rule_max)
    return ((module_min == rule_min) and (module_max == rule_max))