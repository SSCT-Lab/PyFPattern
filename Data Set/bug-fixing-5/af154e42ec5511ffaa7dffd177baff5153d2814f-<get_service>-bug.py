def get_service(self, name):
    raw_data = [service for service in self.client.services(filters={
        'name': name,
    }) if (service['Spec']['Name'] == name)]
    if (len(raw_data) == 0):
        return None
    raw_data = raw_data[0]
    ds = DockerService()
    task_template_data = raw_data['Spec']['TaskTemplate']
    ds.image = task_template_data['ContainerSpec']['Image']
    ds.user = task_template_data['ContainerSpec'].get('User')
    ds.env = task_template_data['ContainerSpec'].get('Env')
    ds.command = task_template_data['ContainerSpec'].get('Command')
    ds.args = task_template_data['ContainerSpec'].get('Args')
    ds.groups = task_template_data['ContainerSpec'].get('Groups')
    ds.stop_signal = task_template_data['ContainerSpec'].get('StopSignal')
    ds.working_dir = task_template_data['ContainerSpec'].get('Dir')
    healthcheck_data = task_template_data['ContainerSpec'].get('Healthcheck')
    if healthcheck_data:
        options = ['test', 'interval', 'timeout', 'start_period', 'retries']
        healthcheck = dict(((key.lower(), value) for (key, value) in healthcheck_data.items() if ((value is not None) and (key.lower() in options))))
        ds.healthcheck = healthcheck
    update_config_data = raw_data['Spec'].get('UpdateConfig')
    if update_config_data:
        ds.update_delay = update_config_data.get('Delay')
        ds.update_parallelism = update_config_data.get('Parallelism')
        ds.update_failure_action = update_config_data.get('FailureAction')
        ds.update_monitor = update_config_data.get('Monitor')
        ds.update_max_failure_ratio = update_config_data.get('MaxFailureRatio')
        ds.update_order = update_config_data.get('Order')
    dns_config = task_template_data['ContainerSpec'].get('DNSConfig')
    if dns_config:
        ds.dns = dns_config.get('Nameservers')
        ds.dns_search = dns_config.get('Search')
        ds.dns_options = dns_config.get('Options')
    ds.hostname = task_template_data['ContainerSpec'].get('Hostname')
    ds.tty = task_template_data['ContainerSpec'].get('TTY')
    placement = task_template_data.get('Placement')
    if placement:
        ds.constraints = placement.get('Constraints')
        placement_preferences = []
        for preference in placement.get('Preferences', []):
            placement_preferences.append(dict(((key.lower(), value['SpreadDescriptor']) for (key, value) in preference.items())))
        ds.placement_preferences = (placement_preferences or None)
    restart_policy_data = task_template_data.get('RestartPolicy')
    if restart_policy_data:
        ds.restart_policy = restart_policy_data.get('Condition')
        ds.restart_policy_delay = restart_policy_data.get('Delay')
        ds.restart_policy_attempts = restart_policy_data.get('MaxAttempts')
        ds.restart_policy_window = restart_policy_data.get('Window')
    raw_data_endpoint_spec = raw_data['Spec'].get('EndpointSpec')
    if raw_data_endpoint_spec:
        ds.endpoint_mode = raw_data_endpoint_spec.get('Mode')
        raw_data_ports = raw_data_endpoint_spec.get('Ports')
        if raw_data_ports:
            ds.publish = []
            for port in raw_data_ports:
                ds.publish.append({
                    'protocol': port['Protocol'],
                    'mode': port.get('PublishMode', None),
                    'published_port': int(port['PublishedPort']),
                    'target_port': int(port['TargetPort']),
                })
    raw_data_limits = task_template_data.get('Resources', {
        
    }).get('Limits')
    if raw_data_limits:
        raw_cpu_limits = raw_data_limits.get('NanoCPUs')
        if raw_cpu_limits:
            ds.limit_cpu = (float(raw_cpu_limits) / 1000000000)
        raw_memory_limits = raw_data_limits.get('MemoryBytes')
        if raw_memory_limits:
            ds.limit_memory = int(raw_memory_limits)
    raw_data_reservations = task_template_data.get('Resources', {
        
    }).get('Reservations')
    if raw_data_reservations:
        raw_cpu_reservations = raw_data_reservations.get('NanoCPUs')
        if raw_cpu_reservations:
            ds.reserve_cpu = (float(raw_cpu_reservations) / 1000000000)
        raw_memory_reservations = raw_data_reservations.get('MemoryBytes')
        if raw_memory_reservations:
            ds.reserve_memory = int(raw_memory_reservations)
    ds.labels = raw_data['Spec'].get('Labels')
    ds.log_driver = task_template_data.get('LogDriver', {
        
    }).get('Name')
    ds.log_driver_options = task_template_data.get('LogDriver', {
        
    }).get('Options')
    ds.container_labels = task_template_data['ContainerSpec'].get('Labels')
    mode = raw_data['Spec']['Mode']
    if ('Replicated' in mode.keys()):
        ds.mode = to_text('replicated', encoding='utf-8')
        ds.replicas = mode['Replicated']['Replicas']
    elif ('Global' in mode.keys()):
        ds.mode = 'global'
    else:
        raise Exception(('Unknown service mode: %s' % mode))
    raw_data_mounts = task_template_data['ContainerSpec'].get('Mounts')
    if raw_data_mounts:
        ds.mounts = []
        for mount_data in raw_data_mounts:
            ds.mounts.append({
                'source': mount_data['Source'],
                'type': mount_data['Type'],
                'target': mount_data['Target'],
                'readonly': mount_data.get('ReadOnly', False),
            })
    raw_data_configs = task_template_data['ContainerSpec'].get('Configs')
    if raw_data_configs:
        ds.configs = []
        for config_data in raw_data_configs:
            ds.configs.append({
                'config_id': config_data['ConfigID'],
                'config_name': config_data['ConfigName'],
                'filename': config_data['File'].get('Name'),
                'uid': int(config_data['File'].get('UID')),
                'gid': int(config_data['File'].get('GID')),
                'mode': config_data['File'].get('Mode'),
            })
    raw_data_secrets = task_template_data['ContainerSpec'].get('Secrets')
    if raw_data_secrets:
        ds.secrets = []
        for secret_data in raw_data_secrets:
            ds.secrets.append({
                'secret_id': secret_data['SecretID'],
                'secret_name': secret_data['SecretName'],
                'filename': secret_data['File'].get('Name'),
                'uid': int(secret_data['File'].get('UID')),
                'gid': int(secret_data['File'].get('GID')),
                'mode': secret_data['File'].get('Mode'),
            })
    networks_names_ids = self.get_networks_names_ids()
    raw_networks_data = task_template_data.get('Networks', raw_data['Spec'].get('Networks'))
    if raw_networks_data:
        ds.networks = []
        for network_data in raw_networks_data:
            network_name = [network_name_id['name'] for network_name_id in networks_names_ids if (network_name_id['id'] == network_data['Target'])]
            if (len(network_name) == 0):
                ds.networks.append(network_data['Target'])
            else:
                ds.networks.append(network_name[0])
    ds.service_version = raw_data['Version']['Index']
    ds.service_id = raw_data['ID']
    return ds