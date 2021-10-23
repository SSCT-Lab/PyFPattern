def __init__(self):
    self.facts = ansible_facts(module)
    self.api_ip = None
    self.fact_paths = {
        'cloudstack_service_offering': 'service-offering',
        'cloudstack_availability_zone': 'availability-zone',
        'cloudstack_public_hostname': 'public-hostname',
        'cloudstack_public_ipv4': 'public-ipv4',
        'cloudstack_local_hostname': 'local-hostname',
        'cloudstack_local_ipv4': 'local-ipv4',
        'cloudstack_instance_id': 'instance-id',
    }