def __init__(self, module):
    super(AnsibleCloudStackFirewall, self).__init__(module)
    self.returns = {
        'cidrlist': 'cidr',
        'startport': 'start_port',
        'endpoint': 'end_port',
        'protocol': 'protocol',
        'ipaddress': 'ip_address',
        'icmpcode': 'icmp_code',
        'icmptype': 'icmp_type',
    }
    self.firewall_rule = None
    self.network = None