def check_for_prefix(self, bucket_name, prefix, delimiter):
    '\n        Checks that a prefix exists in a bucket\n\n        :param bucket_name: the name of the bucket\n        :type bucket_name: str\n        :param prefix: a key prefix\n        :type prefix: str\n        :param delimiter: the delimiter marks key hierarchy.\n        :type delimiter: str\n        '
    prefix = ((prefix + delimiter) if (prefix[(- 1)] != delimiter) else prefix)
    prefix_split = re.split('(\\w+[{d}])$'.format(d=delimiter), prefix, 1)
    previous_level = prefix_split[0]
    plist = self.list_prefixes(bucket_name, previous_level, delimiter)
    return (False if (plist is None) else (prefix in plist))