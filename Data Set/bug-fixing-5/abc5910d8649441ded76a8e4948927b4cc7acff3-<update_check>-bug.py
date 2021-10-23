def update_check(self, entity):
    sched_policy = self._get_sched_policy()
    migration_policy = getattr(entity.migration, 'policy', None)
    return (equal(self.param('comment'), entity.comment) and equal(self.param('description'), entity.description) and equal(self.param('switch_type'), str(entity.switch_type)) and equal(self.param('cpu_arch'), str(entity.cpu.architecture)) and equal(self.param('cpu_type'), entity.cpu.type) and equal(self.param('ballooning'), entity.ballooning_enabled) and equal(self.param('gluster'), entity.gluster_service) and equal(self.param('virt'), entity.virt_service) and equal(self.param('threads_as_cores'), entity.threads_as_cores) and equal(self.param('ksm_numa'), ((not entity.ksm.merge_across_nodes) and entity.ksm.enabled)) and equal(self.param('ksm'), (entity.ksm.merge_across_nodes and entity.ksm.enabled)) and equal(self.param('ha_reservation'), entity.ha_reservation) and equal(self.param('trusted_service'), entity.trusted_service) and equal(self.param('host_reason'), entity.maintenance_reason_required) and equal(self.param('vm_reason'), entity.optional_reason) and equal(self.param('spice_proxy'), getattr(entity.display, 'proxy', None)) and equal(self.param('fence_enabled'), entity.fencing_policy.enabled) and equal(self.param('fence_skip_if_sd_active'), entity.fencing_policy.skip_if_sd_active.enabled) and equal(self.param('fence_skip_if_connectivity_broken'), entity.fencing_policy.skip_if_connectivity_broken.enabled) and equal(self.param('fence_connectivity_threshold'), entity.fencing_policy.skip_if_connectivity_broken.threshold) and equal(self.param('resilience_policy'), str(entity.error_handling.on_error)) and equal(self.param('migration_bandwidth'), str(entity.migration.bandwidth.assignment_method)) and equal(self.param('migration_auto_converge'), str(entity.migration.auto_converge)) and equal(self.param('migration_compressed'), str(entity.migration.compressed)) and equal(self.param('serial_policy'), str(getattr(entity.serial_number, 'policy', None))) and equal(self.param('serial_policy_value'), getattr(entity.serial_number, 'value', None)) and equal(self.param('scheduling_policy'), getattr(self._connection.follow_link(entity.scheduling_policy), 'name', None)) and equal(self._get_policy_id(), getattr(migration_policy, 'id', None)) and equal(self._get_memory_policy(), entity.memory_policy.over_commit.percent) and equal(self.__get_minor(self.param('compatibility_version')), self.__get_minor(entity.version)) and equal(self.__get_major(self.param('compatibility_version')), self.__get_major(entity.version)) and equal((self.param('migration_bandwidth_limit') if (self.param('migration_bandwidth') == 'custom') else None), entity.migration.bandwidth.custom_value) and equal((sorted(self.param('rng_sources')) if self.param('rng_sources') else None), sorted([str(source) for source in entity.required_rng_sources])))