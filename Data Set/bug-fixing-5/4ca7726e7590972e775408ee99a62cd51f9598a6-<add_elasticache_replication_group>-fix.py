def add_elasticache_replication_group(self, replication_group, region):
    ' Adds an ElastiCache replication group to the inventory and index '
    if ((not self.all_elasticache_replication_groups) and (replication_group['Status'] != 'available')):
        return
    if ((replication_group['NodeGroups'][0]['PrimaryEndpoint'] is None) or (replication_group['NodeGroups'][0]['PrimaryEndpoint']['Address'] is None)):
        return
    dest = replication_group['NodeGroups'][0]['PrimaryEndpoint']['Address']
    self.index[dest] = [region, replication_group['ReplicationGroupId']]
    if self.group_by_instance_id:
        self.inventory[replication_group['ReplicationGroupId']] = [dest]
        if self.nested_groups:
            self.push_group(self.inventory, 'instances', replication_group['ReplicationGroupId'])
    if self.group_by_region:
        self.push(self.inventory, region, dest)
        if self.nested_groups:
            self.push_group(self.inventory, 'regions', region)
    if self.group_by_elasticache_engine:
        self.push(self.inventory, 'elasticache_redis', dest)
        if self.nested_groups:
            self.push_group(self.inventory, 'elasticache_engines', 'redis')
    self.push(self.inventory, 'elasticache_replication_groups', replication_group['ReplicationGroupId'])
    host_info = self.get_host_info_dict_from_describe_dict(replication_group)
    self.inventory['_meta']['hostvars'][dest] = host_info