def _host_config(self):
    '\n        Returns parameters used to create a HostConfig object\n        '
    host_config_params = dict(port_bindings='published_ports', publish_all_ports='publish_all_ports', links='links', privileged='privileged', dns='dns_servers', dns_search='dns_search_domains', binds='volume_binds', volumes_from='volumes_from', network_mode='network_mode', cap_add='capabilities', extra_hosts='etc_hosts', read_only='read_only', ipc_mode='ipc_mode', security_opt='security_opts', ulimits='ulimits', sysctls='sysctls', log_config='log_config', mem_limit='memory', memswap_limit='memory_swap', mem_swappiness='memory_swappiness', oom_score_adj='oom_score_adj', oom_kill_disable='oom_killer', shm_size='shm_size', group_add='groups', devices='devices', pid_mode='pid_mode', tmpfs='tmpfs')
    if HAS_DOCKER_PY_2:
        host_config_params['auto_remove'] = 'auto_remove'
    params = dict()
    for (key, value) in host_config_params.items():
        if (getattr(self, value, None) is not None):
            params[key] = getattr(self, value)
    if self.restart_policy:
        params['restart_policy'] = dict(Name=self.restart_policy, MaximumRetryCount=self.restart_retries)
    return self.client.create_host_config(**params)