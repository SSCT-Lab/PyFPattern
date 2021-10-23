def translate_quota(self, quota, parent_quota):
    if six.text_type(quota).endswith('%'):
        pct = int(quota[:(- 1)])
        quota = ((int((parent_quota or 0)) * pct) / 100)
    return _limit_from_settings((quota or parent_quota))