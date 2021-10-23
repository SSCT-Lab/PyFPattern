def store_put(self, key, values):
    key = ((self.prefix + '.d.') + key)
    pipe = self.r.pipeline()
    pipe.delete(key)
    for (k, v) in values.iteritems():
        pipe.hset(key, k, dumps(v))
    pipe.execute()
    return True