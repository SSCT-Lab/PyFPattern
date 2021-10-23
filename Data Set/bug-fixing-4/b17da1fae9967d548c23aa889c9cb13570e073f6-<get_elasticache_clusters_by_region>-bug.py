def get_elasticache_clusters_by_region(self, region):
    " Makes an AWS API call to the list of ElastiCache clusters (with\n        nodes' info) in a particular region."
    try:
        conn = self.connect_to_aws(elasticache, region)
        if conn:
            response = conn.describe_cache_clusters(None, None, None, True)
    except boto.exception.BotoServerError as e:
        error = e.reason
        if (e.error_code == 'AuthFailure'):
            error = self.get_auth_error_message()
        if (not (e.reason == 'Forbidden')):
            error = ('Looks like AWS ElastiCache is down:\n%s' % e.message)
        self.fail_with_error(error, 'getting ElastiCache clusters')
    try:
        clusters = response['DescribeCacheClustersResponse']['DescribeCacheClustersResult']['CacheClusters']
    except KeyError as e:
        error = 'ElastiCache query to AWS failed (unexpected format).'
        self.fail_with_error(error, 'getting ElastiCache clusters')
    for cluster in clusters:
        self.add_elasticache_cluster(cluster, region)