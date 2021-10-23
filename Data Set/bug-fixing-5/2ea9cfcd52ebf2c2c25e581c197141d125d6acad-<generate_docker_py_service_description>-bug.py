def generate_docker_py_service_description(self, name, docker_networks):
    mounts = []
    for mount_config in self.mounts:
        mounts.append(types.Mount(target=mount_config['target'], source=mount_config['source'], type=mount_config['type'], read_only=mount_config['readonly']))
    configs = []
    for config_config in self.configs:
        configs.append(types.ConfigReference(config_id=config_config['config_id'], config_name=config_config['config_name'], filename=config_config.get('filename'), uid=config_config.get('uid'), gid=config_config.get('gid'), mode=config_config.get('mode')))
    secrets = []
    for secret_config in self.secrets:
        secrets.append(types.SecretReference(secret_id=secret_config['secret_id'], secret_name=secret_config['secret_name'], filename=secret_config.get('filename'), uid=secret_config.get('uid'), gid=secret_config.get('gid'), mode=secret_config.get('mode')))
    cspec = types.ContainerSpec(image=self.image, user=self.user, dns_config=types.DNSConfig(nameservers=self.dns, search=self.dns_search, options=self.dns_options), args=self.args, env=self.env, tty=self.tty, hostname=self.hostname, labels=self.container_labels, mounts=mounts, secrets=secrets, configs=configs)
    log_driver = types.DriverConfig(name=self.log_driver, options=self.log_driver_options)
    placement = types.Placement(constraints=self.constraints)
    restart_policy = types.RestartPolicy(condition=self.restart_policy, delay=self.restart_policy_delay, max_attempts=self.restart_policy_attempts, window=self.restart_policy_window)
    resources = types.Resources(cpu_limit=int((self.limit_cpu * 1000000000.0)), mem_limit=self.limit_memory, cpu_reservation=int((self.reserve_cpu * 1000000000.0)), mem_reservation=self.reserve_memory)
    update_policy = types.UpdateConfig(parallelism=self.update_parallelism, delay=self.update_delay, failure_action=self.update_failure_action, monitor=self.update_monitor, max_failure_ratio=self.update_max_failure_ratio, order=self.update_order)
    task_template = types.TaskTemplate(container_spec=cspec, log_driver=log_driver, restart_policy=restart_policy, placement=placement, resources=resources, force_update=self.force_update)
    if (self.mode == 'global'):
        self.replicas = None
    mode = types.ServiceMode(self.mode, replicas=self.replicas)
    networks = []
    for network_name in self.networks:
        network_id = None
        try:
            network_id = filter((lambda n: (n['name'] == network_name)), docker_networks)[0]['id']
        except:
            pass
        if network_id:
            networks.append({
                'Target': network_id,
            })
        else:
            raise Exception(('no docker networks named: %s' % network_name))
    ports = {
        
    }
    for port in self.publish:
        ports[int(port['published_port'])] = (int(port['target_port']), port['protocol'], port['mode'])
    endpoint_spec = types.EndpointSpec(mode=self.endpoint_mode, ports=ports)
    return (update_policy, task_template, networks, endpoint_spec, mode, self.labels)