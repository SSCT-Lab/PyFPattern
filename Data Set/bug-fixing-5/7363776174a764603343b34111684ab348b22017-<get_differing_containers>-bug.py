def get_differing_containers(self):
    '\n        Inspect all matching, running containers, and return those that were\n        started with parameters that differ from the ones that are provided\n        during this module run. A list containing the differing\n        containers will be returned, and a short string describing the specific\n        difference encountered in each container will be appended to\n        reload_reasons.\n\n        This generates the set of containers that need to be stopped and\n        started with new parameters with state=reloaded.\n        '
    running = self.get_running_containers()
    current = self.get_inspect_containers(running)
    defaults = self.client.info()
    api_version = self.client.version()['ApiVersion']
    image = self.get_inspect_image()
    if (image is None):
        return current
    differing = []
    for container in current:
        if (container['Image'] != image['Id']):
            self.reload_reasons.append('image ({0} => {1})'.format(container['Image'], image['Id']))
            differing.append(container)
            continue
        expected_entrypoint = self.module.params.get('entrypoint')
        if expected_entrypoint:
            expected_entrypoint = shlex.split(expected_entrypoint)
            actual_entrypoint = container['Config']['Entrypoint']
            if (actual_entrypoint != expected_entrypoint):
                self.reload_reasons.append('entrypoint ({0} => {1})'.format(actual_entrypoint, expected_entrypoint))
                differing.append(container)
                continue
        expected_command = self.module.params.get('command')
        if expected_command:
            expected_command = shlex.split(expected_command)
            actual_command = container['Config']['Cmd']
            if (actual_command != expected_command):
                self.reload_reasons.append('command ({0} => {1})'.format(actual_command, expected_command))
                differing.append(container)
                continue
        expected_exposed_ports = set((image['ContainerConfig'].get('ExposedPorts') or {
            
        }).keys())
        for p in (self.exposed_ports or []):
            expected_exposed_ports.add('/'.join(p))
        actually_exposed_ports = set((container['Config'].get('ExposedPorts') or {
            
        }).keys())
        if (actually_exposed_ports != expected_exposed_ports):
            self.reload_reasons.append('exposed_ports ({0} => {1})'.format(actually_exposed_ports, expected_exposed_ports))
            differing.append(container)
            continue
        expected_volume_keys = set((image['ContainerConfig']['Volumes'] or {
            
        }).keys())
        if self.volumes:
            expected_volume_keys.update(self.volumes)
        actual_volume_keys = set((container['Config']['Volumes'] or {
            
        }).keys())
        if (actual_volume_keys != expected_volume_keys):
            self.reload_reasons.append('volumes ({0} => {1})'.format(actual_volume_keys, expected_volume_keys))
            differing.append(container)
            continue
        expected_ulimit_keys = set(map((lambda x: ('%s:%s:%s' % (x['name'], x['soft'], x['hard']))), (self.ulimits or [])))
        actual_ulimit_keys = set(map((lambda x: ('%s:%s:%s' % (x['Name'], x['Soft'], x['Hard']))), (container['HostConfig']['Ulimits'] or [])))
        if (actual_ulimit_keys != expected_ulimit_keys):
            self.reload_reasons.append('ulimits ({0} => {1})'.format(actual_ulimit_keys, expected_ulimit_keys))
            differing.append(container)
            continue
        expected_cpu_shares = self.module.params.get('cpu_shares')
        actual_cpu_shares = container['HostConfig']['CpuShares']
        if (expected_cpu_shares and (actual_cpu_shares != expected_cpu_shares)):
            self.reload_reasons.append('cpu_shares ({0} => {1})'.format(actual_cpu_shares, expected_cpu_shares))
            differing.append(container)
            continue
        try:
            expected_mem = _human_to_bytes(self.module.params.get('memory_limit'))
        except ValueError as e:
            self.module.fail_json(msg=str(e))
        if (docker.utils.compare_version('1.19', api_version) >= 0):
            actual_mem = container['HostConfig']['Memory']
        else:
            actual_mem = container['Config']['Memory']
        if (expected_mem and (actual_mem != expected_mem)):
            self.reload_reasons.append('memory ({0} => {1})'.format(actual_mem, expected_mem))
            differing.append(container)
            continue
        expected_env = {
            
        }
        for image_env in (image['ContainerConfig']['Env'] or []):
            (name, value) = image_env.split('=', 1)
            expected_env[name] = value
        if self.environment:
            for (name, value) in self.environment.items():
                expected_env[name] = str(value)
        actual_env = {
            
        }
        for container_env in (container['Config']['Env'] or []):
            (name, value) = container_env.split('=', 1)
            actual_env[name] = value
        if (actual_env != expected_env):
            self.reload_reasons.append('environment {0} => {1}'.format(actual_env, expected_env))
            differing.append(container)
            continue
        expected_labels = {
            
        }
        for (name, value) in self.module.params.get('labels').items():
            expected_labels[name] = str(value)
        if isinstance(container['Config']['Labels'], dict):
            actual_labels = container['Config']['Labels']
        else:
            for container_label in (container['Config']['Labels'] or []):
                (name, value) = container_label.split('=', 1)
                actual_labels[name] = value
        if (actual_labels != expected_labels):
            self.reload_reasons.append('labels {0} => {1}'.format(actual_labels, expected_labels))
            differing.append(container)
            continue
        expected_hostname = self.module.params.get('hostname')
        actual_hostname = container['Config']['Hostname']
        if (expected_hostname and (actual_hostname != expected_hostname)):
            self.reload_reasons.append('hostname ({0} => {1})'.format(actual_hostname, expected_hostname))
            differing.append(container)
            continue
        expected_domainname = self.module.params.get('domainname')
        actual_domainname = container['Config']['Domainname']
        if (expected_domainname and (actual_domainname != expected_domainname)):
            self.reload_reasons.append('domainname ({0} => {1})'.format(actual_domainname, expected_domainname))
            differing.append(container)
            continue
        expected_stdin_open = self.module.params.get('stdin_open')
        actual_stdin_open = container['Config']['OpenStdin']
        if (actual_stdin_open != expected_stdin_open):
            self.reload_reasons.append('stdin_open ({0} => {1})'.format(actual_stdin_open, expected_stdin_open))
            differing.append(container)
            continue
        expected_tty = self.module.params.get('tty')
        actual_tty = container['Config']['Tty']
        if (actual_tty != expected_tty):
            self.reload_reasons.append('tty ({0} => {1})'.format(actual_tty, expected_tty))
            differing.append(container)
            continue
        if self.lxc_conf:
            expected_lxc = set(self.lxc_conf)
            actual_lxc = set((container['HostConfig']['LxcConf'] or []))
            if (actual_lxc != expected_lxc):
                self.reload_reasons.append('lxc_conf ({0} => {1})'.format(actual_lxc, expected_lxc))
                differing.append(container)
                continue
        expected_binds = set()
        if self.binds:
            for bind in self.binds:
                expected_binds.add(bind)
        actual_binds = set()
        for bind in (container['HostConfig']['Binds'] or []):
            if (len(bind.split(':')) == 2):
                actual_binds.add((bind + ':rw'))
            else:
                actual_binds.add(bind)
        if (actual_binds != expected_binds):
            self.reload_reasons.append('binds ({0} => {1})'.format(actual_binds, expected_binds))
            differing.append(container)
            continue
        expected_bound_ports = {
            
        }
        if self.port_bindings:
            for (container_port, config) in self.port_bindings.items():
                if isinstance(container_port, int):
                    container_port = '{0}/tcp'.format(container_port)
                if (len(config) == 1):
                    expected_bound_ports[container_port] = [{
                        'HostIp': '0.0.0.0',
                        'HostPort': '',
                    }]
                elif isinstance(config[0], tuple):
                    expected_bound_ports[container_port] = []
                    for (hostip, hostport) in config:
                        expected_bound_ports[container_port].append({
                            'HostIp': hostip,
                            'HostPort': str(hostport),
                        })
                else:
                    expected_bound_ports[container_port] = [{
                        'HostIp': config[0],
                        'HostPort': str(config[1]),
                    }]
        actual_bound_ports = (container['HostConfig']['PortBindings'] or {
            
        })
        if (actual_bound_ports != expected_bound_ports):
            self.reload_reasons.append('port bindings ({0} => {1})'.format(actual_bound_ports, expected_bound_ports))
            differing.append(container)
            continue
        expected_privileged = self.module.params.get('privileged')
        actual_privileged = container['HostConfig']['Privileged']
        if (actual_privileged != expected_privileged):
            self.reload_reasons.append('privileged ({0} => {1})'.format(actual_privileged, expected_privileged))
            differing.append(container)
            continue
        expected_links = set()
        for (link, alias) in (self.links or {
            
        }).items():
            expected_links.add('/{0}:{1}/{2}'.format(link, container['Name'], alias))
        actual_links = set((container['HostConfig']['Links'] or []))
        if (actual_links != expected_links):
            self.reload_reasons.append('links ({0} => {1})'.format(actual_links, expected_links))
            differing.append(container)
            continue
        expected_netmode = (self.module.params.get('net') or 'bridge')
        actual_netmode = (container['HostConfig']['NetworkMode'] or 'bridge')
        if (actual_netmode != expected_netmode):
            self.reload_reasons.append('net ({0} => {1})'.format(actual_netmode, expected_netmode))
            differing.append(container)
            continue
        expected_devices = set()
        for device in (self.module.params.get('devices') or []):
            if (len(device.split(':')) == 2):
                expected_devices.add((device + ':rwm'))
            else:
                expected_devices.add(device)
        actual_devices = set()
        for device in (container['HostConfig']['Devices'] or []):
            actual_devices.add('{PathOnHost}:{PathInContainer}:{CgroupPermissions}'.format(**device))
        if (actual_devices != expected_devices):
            self.reload_reasons.append('devices ({0} => {1})'.format(actual_devices, expected_devices))
            differing.append(container)
            continue
        expected_dns = set((self.module.params.get('dns') or []))
        actual_dns = set((container['HostConfig']['Dns'] or []))
        if (actual_dns != expected_dns):
            self.reload_reasons.append('dns ({0} => {1})'.format(actual_dns, expected_dns))
            differing.append(container)
            continue
        expected_volumes_from = set((self.module.params.get('volumes_from') or []))
        actual_volumes_from = set((container['HostConfig']['VolumesFrom'] or []))
        if (actual_volumes_from != expected_volumes_from):
            self.reload_reasons.append('volumes_from ({0} => {1})'.format(actual_volumes_from, expected_volumes_from))
            differing.append(container)
        if self.ensure_capability('log_driver', False):
            expected_log_driver = (self.module.params.get('log_driver') or defaults['LoggingDriver'])
            actual_log_driver = container['HostConfig']['LogConfig']['Type']
            if (actual_log_driver != expected_log_driver):
                self.reload_reasons.append('log_driver ({0} => {1})'.format(actual_log_driver, expected_log_driver))
                differing.append(container)
                continue
        if self.ensure_capability('log_opt', False):
            expected_logging_opts = (self.module.params.get('log_opt') or {
                
            })
            actual_log_opts = container['HostConfig']['LogConfig']['Config']
            if (len((set(expected_logging_opts.items()) - set(actual_log_opts.items()))) != 0):
                log_opt_reasons = {
                    'added': dict((set(expected_logging_opts.items()) - set(actual_log_opts.items()))),
                    'removed': dict((set(actual_log_opts.items()) - set(expected_logging_opts.items()))),
                }
                self.reload_reasons.append('log_opt ({0})'.format(log_opt_reasons))
                differing.append(container)
    return differing