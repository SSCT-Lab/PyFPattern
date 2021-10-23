def has_different_resource_limits(self):
    '\n        Diff parameters and container resource limits\n        '
    if (not self.container.get('HostConfig')):
        self.fail('limits_differ_from_container: Error parsing container properties. HostConfig missing.')
    host_config = self.container['HostConfig']
    config_mapping = dict(cpu_period=host_config.get('CpuPeriod'), cpu_quota=host_config.get('CpuQuota'), cpuset_cpus=host_config.get('CpusetCpus'), cpuset_mems=host_config.get('CpusetMems'), kernel_memory=host_config.get('KernelMemory'), memory=host_config.get('Memory'), memory_reservation=host_config.get('MemoryReservation'), memory_swap=host_config.get('MemorySwap'), oom_score_adj=host_config.get('OomScoreAdj'), oom_killer=host_config.get('OomKillDisable'))
    if HAS_DOCKER_PY_3:
        config_mapping['cpu_shares'] = host_config.get('CpuShares')
    differences = []
    for (key, value) in config_mapping.items():
        if (getattr(self.parameters, key, None) and (getattr(self.parameters, key) != value)):
            item = dict()
            item[key] = dict(parameter=getattr(self.parameters, key), container=value)
            differences.append(item)
    different = (len(differences) > 0)
    return (different, differences)