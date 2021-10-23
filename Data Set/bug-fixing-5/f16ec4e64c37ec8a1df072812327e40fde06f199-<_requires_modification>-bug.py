def _requires_modification(self):
    'Check if cluster requires (nondestructive) modification'
    modifiable_data = {
        'NumCacheNodes': self.num_nodes,
        'EngineVersion': self.cache_engine_version,
    }
    for (key, value) in modifiable_data.items():
        if ((value is not None) and (self.data[key] != value)):
            return True
    cache_security_groups = []
    for sg in self.data['CacheSecurityGroups']:
        cache_security_groups.append(sg['CacheSecurityGroupName'])
    if (set(cache_security_groups) != set(self.cache_security_groups)):
        return True
    if self.security_group_ids:
        vpc_security_groups = []
        security_groups = (self.data['SecurityGroups'] or [])
        for sg in security_groups:
            vpc_security_groups.append(sg['SecurityGroupId'])
        if (set(vpc_security_groups) != set(self.security_group_ids)):
            return True
    return False