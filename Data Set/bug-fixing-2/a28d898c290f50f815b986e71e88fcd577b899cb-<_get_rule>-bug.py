

def _get_rule(self, rules):
    user_security_group_name = self.module.params.get('user_security_group')
    cidr = self.module.params.get('cidr')
    protocol = self.module.params.get('protocol')
    start_port = self.module.params.get('start_port')
    end_port = self.get_or_fallback('end_port', 'start_port')
    icmp_code = self.module.params.get('icmp_code')
    icmp_type = self.module.params.get('icmp_type')
    if ((protocol in ['tcp', 'udp']) and (not (start_port and end_port))):
        self.module.fail_json(msg=("no start_port or end_port set for protocol '%s'" % protocol))
    if ((protocol == 'icmp') and (not (icmp_type and icmp_code))):
        self.module.fail_json(msg=("no icmp_type or icmp_code set for protocol '%s'" % protocol))
    for rule in rules:
        if user_security_group_name:
            type_match = self._type_security_group_match(rule, user_security_group_name)
        else:
            type_match = self._type_cidr_match(rule, cidr)
        protocol_match = (self._tcp_udp_match(rule, protocol, start_port, end_port) or self._icmp_match(rule, protocol, icmp_code, icmp_type) or self._ah_esp_gre_match(rule, protocol))
        if (type_match and protocol_match):
            return rule
    return None
