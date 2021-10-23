

def get_service(self, name):
    raw_data = [service for service in self.client.services(filters={
        'name': name,
    }) if (service['Spec']['Name'] == name)]
    if (len(raw_data) == 0):
        return None
    raw_data = raw_data[0]
    networks_names_ids = self.get_networks_names_ids()
    ds = DockerService()
    task_template_data = raw_data['Spec']['TaskTemplate']
    update_config_data = raw_data['Spec']['UpdateConfig']
    ds.image = task_template_data['ContainerSpec']['Image']
    ds.user = task_template_data['ContainerSpec'].get('User', None)
    ds.env = task_template_data['ContainerSpec'].get('Env', [])
    ds.command = task_template_data['ContainerSpec'].get('Command')
    ds.args = task_template_data['ContainerSpec'].get('Args', [])
    ds.update_delay = update_config_data['Delay']
    ds.update_parallelism = update_config_data['Parallelism']
    ds.update_failure_action = update_config_data['FailureAction']
    ds.update_monitor = update_config_data['Monitor']
    ds.update_max_failure_ratio = update_config_data['MaxFailureRatio']
    if ('Order' in update_config_data):
        ds.update_order = update_config_data['Order']
    dns_config = task_template_data['ContainerSpec'].get('DNSConfig', None)
    if dns_config:
        if ('Nameservers' in dns_config.keys()):
            ds.dns = dns_config['Nameservers']
        if ('Search' in dns_config.keys()):
            ds.dns_search = dns_config['Search']
        if ('Options' in dns_config.keys()):
            ds.dns_options = dns_config['Options']
    ds.hostname = task_template_data['ContainerSpec'].get('Hostname', '')
    ds.tty = task_template_data['ContainerSpec'].get('TTY', False)
    if ('Placement' in task_template_data.keys()):
        placement = task_template_data['Placement']
        ds.constraints = placement.get('Constraints', [])
        placement_preferences = []
        for preference in placement.get('Preferences', []):
            placement_preferences.append(dict(((key.lower(), value['SpreadDescriptor']) for (key, value) in preference.items())))
        ds.placement_preferences = (placement_preferences or None)
    restart_policy_data = task_template_data.get('RestartPolicy', None)
    if restart_policy_data:
        ds.restart_policy = restart_policy_data.get('Condition')
        ds.restart_policy_delay = restart_policy_data.get('Delay')
        ds.restart_policy_attempts = restart_policy_data.get('MaxAttempts')
        ds.restart_policy_window = restart_policy_data.get('Window')
    raw_data_endpoint_spec = raw_data['Spec'].get('EndpointSpec')
    if raw_data_endpoint_spec:
        ds.endpoint_mode = raw_data_endpoint_spec.get('Mode')
        for port in raw_data_endpoint_spec.get('Ports', []):
            ds.publish.append({
                'protocol': port['Protocol'],
                'mode': port.get('PublishMode', None),
                'published_port': int(port['PublishedPort']),
                'target_port': int(port['TargetPort']),
            })
    if ('Resources' in task_template_data.keys()):
        if ('Limits' in task_template_data['Resources'].keys()):
            if ('NanoCPUs' in task_template_data['Resources']['Limits'].keys()):
                ds.limit_cpu = (float(task_template_data['Resources']['Limits']['NanoCPUs']) / 1000000000)
            if ('MemoryBytes' in task_template_data['Resources']['Limits'].keys()):
                ds.limit_memory = int(task_template_data['Resources']['Limits']['MemoryBytes'])
        if ('Reservations' in task_template_data['Resources'].keys()):
            if ('NanoCPUs' in task_template_data['Resources']['Reservations'].keys()):
                ds.reserve_cpu = (float(task_template_data['Resources']['Reservations']['NanoCPUs']) / 1000000000)
            if ('MemoryBytes' in task_template_data['Resources']['Reservations'].keys()):
                ds.reserve_memory = int(task_template_data['Resources']['Reservations']['MemoryBytes'])
    ds.labels = raw_data['Spec'].get('Labels', {
        
    })
    if ('LogDriver' in task_template_data.keys()):
        ds.log_driver = task_template_data['LogDriver'].get('Name', 'json-file')
        ds.log_driver_options = task_template_data['LogDriver'].get('Options', {
            
        })
    ds.container_labels = task_template_data['ContainerSpec'].get('Labels', {
        
    })
    mode = raw_data['Spec']['Mode']
    if ('Replicated' in mode.keys()):
        ds.mode = to_text('replicated', encoding='utf-8')
        ds.replicas = mode['Replicated']['Replicas']
    elif ('Global' in mode.keys()):
        ds.mode = 'global'
    else:
        raise Exception(('Unknown service mode: %s' % mode))
    for mount_data in raw_data['Spec']['TaskTemplate']['ContainerSpec'].get('Mounts', []):
        ds.mounts.append({
            'source': mount_data['Source'],
            'type': mount_data['Type'],
            'target': mount_data['Target'],
            'readonly': mount_data.get('ReadOnly', False),
        })
    for config_data in raw_data['Spec']['TaskTemplate']['ContainerSpec'].get('Configs', []):
        ds.configs.append({
            'config_id': config_data['ConfigID'],
            'config_name': config_data['ConfigName'],
            'filename': config_data['File'].get('Name'),
            'uid': int(config_data['File'].get('UID')),
            'gid': int(config_data['File'].get('GID')),
            'mode': config_data['File'].get('Mode'),
        })
    for secret_data in raw_data['Spec']['TaskTemplate']['ContainerSpec'].get('Secrets', []):
        ds.secrets.append({
            'secret_id': secret_data['SecretID'],
            'secret_name': secret_data['SecretName'],
            'filename': secret_data['File'].get('Name'),
            'uid': int(secret_data['File'].get('UID')),
            'gid': int(secret_data['File'].get('GID')),
            'mode': secret_data['File'].get('Mode'),
        })
    networks_names_ids = self.get_networks_names_ids()
    for raw_network_data in raw_data['Spec']['TaskTemplate'].get('Networks', raw_data['Spec'].get('Networks', [])):
        network_name = [network_name_id['name'] for network_name_id in networks_names_ids if (network_name_id['id'] == raw_network_data['Target'])]
        if (len(network_name) == 0):
            ds.networks.append(raw_network_data['Target'])
        else:
            ds.networks.append(network_name[0])
    ds.service_version = raw_data['Version']['Index']
    ds.service_id = raw_data['ID']
    return ds
