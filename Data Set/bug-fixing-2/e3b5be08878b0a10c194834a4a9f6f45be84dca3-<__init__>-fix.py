

def __init__(self, module):
    super(AnsibleVultrServer, self).__init__(module, 'vultr_server')
    self.server = None
    self.returns = {
        'SUBID': dict(key='id'),
        'label': dict(key='name'),
        'date_created': dict(),
        'allowed_bandwidth_gb': dict(convert_to='int'),
        'auto_backups': dict(key='auto_backup_enabled', convert_to='bool'),
        'current_bandwidth_gb': dict(),
        'kvm_url': dict(),
        'default_password': dict(),
        'internal_ip': dict(),
        'disk': dict(),
        'cost_per_month': dict(convert_to='float'),
        'location': dict(key='region'),
        'main_ip': dict(key='v4_main_ip'),
        'network_v4': dict(key='v4_network'),
        'gateway_v4': dict(key='v4_gateway'),
        'os': dict(),
        'pending_charges': dict(convert_to='float'),
        'power_status': dict(),
        'ram': dict(),
        'plan': dict(),
        'server_state': dict(),
        'status': dict(),
        'firewall_group': dict(),
        'tag': dict(),
        'v6_main_ip': dict(),
        'v6_network': dict(),
        'v6_network_size': dict(),
        'v6_networks': dict(),
        'vcpu_count': dict(convert_to='int'),
    }
    self.server_power_state = None
