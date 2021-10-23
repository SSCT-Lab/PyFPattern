def __init__(self, project=None, instance='sentry', table='nodestore', automatic_expiry=False, default_ttl=None, compression=False, thread_pool_size=5, **kwargs):
    self.project = project
    self.instance = instance
    self.table = table
    self.options = kwargs
    self.automatic_expiry = automatic_expiry
    self.default_ttl = default_ttl
    self.compression = compression
    self.skip_deletes = (automatic_expiry and ('_SENTRY_CLEANUP' in os.environ))