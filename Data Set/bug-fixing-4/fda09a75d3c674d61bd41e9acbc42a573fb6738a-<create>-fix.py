def create(self):
    'Create an ElastiCache cluster'
    if (self.status == 'available'):
        return
    if (self.status in ['creating', 'rebooting', 'modifying']):
        if self.wait:
            self._wait_for_status('available')
        return
    if (self.status == 'deleting'):
        if self.wait:
            self._wait_for_status('gone')
        else:
            msg = "'%s' is currently deleting. Cannot create."
            self.module.fail_json(msg=(msg % self.name))
    kwargs = dict(CacheClusterId=self.name, NumCacheNodes=self.num_nodes, CacheNodeType=self.node_type, Engine=self.engine, EngineVersion=self.cache_engine_version, CacheSecurityGroupNames=self.cache_security_groups, SecurityGroupIds=self.security_group_ids, CacheParameterGroupName=self.cache_parameter_group, CacheSubnetGroupName=self.cache_subnet_group)
    if (self.cache_port is not None):
        kwargs['Port'] = self.cache_port
    if (self.zone is not None):
        kwargs['PreferredAvailabilityZone'] = self.zone
    try:
        self.conn.create_cache_cluster(**kwargs)
    except botocore.exceptions.ClientError as e:
        self.module.fail_json(msg=e.message, exception=format_exc(), **camel_dict_to_snake_dict(e.response))
    self._refresh_data()
    self.changed = True
    if self.wait:
        self._wait_for_status('available')
    return True