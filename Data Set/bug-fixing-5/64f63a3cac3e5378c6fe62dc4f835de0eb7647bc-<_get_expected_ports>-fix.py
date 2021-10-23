def _get_expected_ports(self):
    if (not self.parameters.published_ports):
        return None
    expected_bound_ports = {
        
    }
    for (container_port, config) in self.parameters.published_ports.items():
        if isinstance(container_port, int):
            container_port = ('%s/tcp' % container_port)
        if (len(config) == 1):
            if isinstance(config[0], int):
                expected_bound_ports[container_port] = [{
                    'HostIp': '0.0.0.0',
                    'HostPort': config[0],
                }]
            else:
                expected_bound_ports[container_port] = [{
                    'HostIp': config[0],
                    'HostPort': '',
                }]
        elif isinstance(config[0], tuple):
            expected_bound_ports[container_port] = []
            for (host_ip, host_port) in config:
                expected_bound_ports[container_port].append({
                    'HostIp': host_ip,
                    'HostPort': str(host_port),
                })
        else:
            expected_bound_ports[container_port] = [{
                'HostIp': config[0],
                'HostPort': str(config[1]),
            }]
    return expected_bound_ports