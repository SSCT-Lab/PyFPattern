def _get_elasticache_connection(self):
    'Get an elasticache connection'
    try:
        endpoint = ('elasticache.%s.amazonaws.com' % self.region)
        connect_region = RegionInfo(name=self.region, endpoint=endpoint)
        return ElastiCacheConnection(region=connect_region, **self.aws_connect_kwargs)
    except boto.exception.NoAuthHandlerFound as e:
        self.module.fail_json(msg=e.message)