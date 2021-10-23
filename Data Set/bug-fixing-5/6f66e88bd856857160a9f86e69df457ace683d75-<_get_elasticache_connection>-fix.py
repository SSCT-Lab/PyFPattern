def _get_elasticache_connection(self):
    'Get an elasticache connection'
    try:
        return connect_to_region(region_name=self.region, **self.aws_connect_kwargs)
    except boto.exception.NoAuthHandlerFound as e:
        self.module.fail_json(msg=e.message)