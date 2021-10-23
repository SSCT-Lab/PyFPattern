def is_rate_limited(self, project, key=None, timestamp=None):
    if (timestamp is None):
        timestamp = time()
    quotas = self.get_quotas_with_limits(project, key=key)
    if (not quotas):
        return NotRateLimited()
    keys = []
    args = []
    for quota in quotas:
        shift = (project.organization_id % quota.window)
        key = self.__get_redis_key(quota, timestamp, shift, project.organization_id)
        return_key = self.get_refunded_quota_key(key)
        keys.extend((key, return_key))
        expiry = (self.get_next_period_start(quota.window, shift, timestamp) + self.grace)
        args.extend((quota.limit, int(expiry)))
    client = self.__get_redis_client(six.text_type(project.organization_id))
    rejections = is_rate_limited(client, keys, args)
    if any(rejections):
        enforce = False
        worst_case = (0, None)
        for (quota, rejected) in zip(quotas, rejections):
            if (not rejected):
                continue
            if quota.enforce:
                enforce = True
                shift = (project.organization_id % quota.window)
                delay = (self.get_next_period_start(quota.window, shift, timestamp) - timestamp)
                if (delay > worst_case[0]):
                    worst_case = (delay, quota.reason_code)
        if enforce:
            return RateLimited(retry_after=worst_case[0], reason_code=worst_case[1])
    return NotRateLimited()