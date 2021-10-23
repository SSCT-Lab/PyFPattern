def check_for_wildcard_key(self, wildcard_key, bucket_name=None, delimiter=''):
    '\n        Checks that a key matching a wildcard expression exists in a bucket\n        '
    return (self.get_wildcard_key(wildcard_key=wildcard_key, bucket_name=bucket_name, delimiter=delimiter) is not None)