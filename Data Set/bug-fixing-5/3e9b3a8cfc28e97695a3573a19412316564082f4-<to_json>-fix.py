def to_json(self):
    return prune_empty_keys({
        'prefix': six.text_type(self.prefix),
        'subscope': (six.text_type(self.subscope) if (self.subscope is not None) else None),
        'limit': self.limit,
        'window': self.window,
        'reasonCode': self.reason_code,
    })