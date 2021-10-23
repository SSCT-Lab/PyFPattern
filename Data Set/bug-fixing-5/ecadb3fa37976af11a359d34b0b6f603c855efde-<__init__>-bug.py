def __init__(self, **options):
    self.dummy = DummyTSDB()
    self.redis = RedisTSDB(**options.get('redis', {
        
    }))
    self.snuba = SnubaTSDB(**options.get('snuba', {
        
    }))