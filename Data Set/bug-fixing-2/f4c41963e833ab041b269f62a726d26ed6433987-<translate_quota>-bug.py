

def translate_quota(self, quota, parent_quota):
    if six.text_type(quota).endswith('%'):
        pct = int(quota[:(- 1)])
        quota = ((int(parent_quota) * pct) / 100)
    if (not quota):
        return _limit_from_settings(parent_quota)
    return _limit_from_settings(quota)
