def refund(self, project, key=None, timestamp=None):
    if (timestamp is None):
        timestamp = time()
    quotas = self.get_quotas_with_limits(project, key=key)
    if (not quotas):
        return
    client = self.cluster.get_local_client_for_key(six.text_type(project.organization_id))
    pipe = client.pipeline()
    for quota in quotas:
        shift = (project.organization_id % quota.window)
        expiry = (self.get_next_period_start(quota.window, shift, timestamp) + self.grace)
        return_key = self.get_refunded_quota_key(self.__get_redis_key(quota, timestamp, shift, project.organization_id))
        pipe.incr(return_key, 1)
        pipe.expireat(return_key, int(expiry))
    pipe.execute()