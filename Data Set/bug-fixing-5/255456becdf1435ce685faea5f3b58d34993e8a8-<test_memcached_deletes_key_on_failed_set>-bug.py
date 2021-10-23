def test_memcached_deletes_key_on_failed_set(self):
    max_value_length = getattr(cache._lib, 'SERVER_MAX_VALUE_LENGTH', 1048576)
    cache.set('small_value', 'a')
    self.assertEqual(cache.get('small_value'), 'a')
    large_value = ('a' * (max_value_length + 1))
    cache.set('small_value', large_value)
    value = cache.get('small_value')
    self.assertTrue(((value is None) or (value == large_value)))