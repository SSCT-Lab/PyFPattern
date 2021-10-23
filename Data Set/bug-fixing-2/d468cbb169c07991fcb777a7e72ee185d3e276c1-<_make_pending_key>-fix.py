

def _make_pending_key(self, partition=None):
    "\n        Returns the key to be used for the pending buffer.\n        When partitioning is enabled, there is a key for each\n        partition, without it, there's only the default pending_key\n        "
    if (partition is None):
        return self.pending_key
    assert (partition >= 0)
    return ('%s:%d' % (self.pending_key, partition))
