def test_long_timeout(self):
    "\n        Followe memcached's convention where a timeout greater than 30 days is\n        treated as an absolute expiration timestamp instead of a relative\n        offset (#12399).\n        "
    cache.set('key1', 'eggs', ((((60 * 60) * 24) * 30) + 1))
    self.assertEqual(cache.get('key1'), 'eggs')
    cache.add('key2', 'ham', ((((60 * 60) * 24) * 30) + 1))
    self.assertEqual(cache.get('key2'), 'ham')
    cache.set_many({
        'key3': 'sausage',
        'key4': 'lobster bisque',
    }, ((((60 * 60) * 24) * 30) + 1))
    self.assertEqual(cache.get('key3'), 'sausage')
    self.assertEqual(cache.get('key4'), 'lobster bisque')