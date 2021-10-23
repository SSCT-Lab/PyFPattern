@staticmethod
def normalize_rule_set(rule_obj):
    rule_dict = dict()
    rule_dict['key'] = rule_obj.key
    rule_dict['service'] = rule_obj.service
    rule_dict['enabled'] = rule_obj.enabled
    rule_dict['rule'] = []
    for rule in rule_obj.rule:
        rule_set_dict = dict()
        rule_set_dict['port'] = rule.port
        rule_set_dict['end_port'] = rule.endPort
        rule_set_dict['direction'] = rule.direction
        rule_set_dict['port_type'] = rule.portType
        rule_set_dict['protocol'] = rule.protocol
        rule_dict['rule'].append(rule_set_dict)
    allowed_host = rule_obj.allowedHosts
    rule_allow_host = dict()
    rule_allow_host['ip_address'] = [ip for ip in allowed_host.ipAddress]
    rule_allow_host['all_ip'] = allowed_host.allIp
    rule_dict['allowed_hosts'] = rule_allow_host
    return rule_dict