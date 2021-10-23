def get_wildcard_key(self, wildcard_key, bucket_name=None, delimiter=''):
    '\n        Returns a boto3.s3.Object object matching the wildcard expression\n\n        :param wildcard_key: the path to the key\n        :type wildcard_key: str\n        :param bucket_name: the name of the bucket\n        :type bucket_name: str\n        '
    if (not bucket_name):
        (bucket_name, wildcard_key) = self.parse_s3_url(wildcard_key)
    prefix = re.split('[*]', wildcard_key, 1)[0]
    klist = self.list_keys(bucket_name, prefix=prefix, delimiter=delimiter)
    if klist:
        key_matches = [k for k in klist if fnmatch.fnmatch(k, wildcard_key)]
        if key_matches:
            return self.get_key(key_matches[0], bucket_name)