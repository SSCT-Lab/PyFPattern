def to_json(self):
    return prune_empty_keys({
        'prefix': self.prefix,
        'subscope': self.subscope,
        'limit': self.limit,
        'window': self.window,
        'reasonCode': self.reason_code,
    })