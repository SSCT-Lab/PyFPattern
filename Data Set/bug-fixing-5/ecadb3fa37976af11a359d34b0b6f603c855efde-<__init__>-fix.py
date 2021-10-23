def __init__(self, **options):
    self.dummy = DummyTSDB()
    self.redis = RedisTSDB(**options.pop('redis', {
        
    }))
    self.snuba = SnubaTSDB(**options.pop('snuba', {
        
    }))
    super(RedisSnubaTSDB, self).__init__(**options)