@property
def update_parameters(self):
    '\n        Returns parameters used to update a container\n        '
    update_parameters = dict(blkio_weight='blkio_weight', cpu_period='cpu_period', cpu_quota='cpu_quota', cpu_shares='cpu_shares', cpuset_cpus='cpuset_cpus', mem_limit='memory', mem_reservation='mem_reservation', memswap_limit='memory_swap', kernel_memory='kernel_memory')
    result = dict()
    for (key, value) in update_parameters.items():
        if (getattr(self, value, None) is not None):
            result[key] = getattr(self, value)
    return result