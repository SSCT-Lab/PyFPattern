def include_rds_clusters_by_region(self, region):
    if (not HAS_BOTO3):
        self.fail_with_error('Working with RDS clusters requires boto3 - please install boto3 and try again', 'getting RDS clusters')
    client = ec2_utils.boto3_inventory_conn('client', 'rds', region, **self.credentials)
    (marker, clusters) = ('', [])
    while (marker is not None):
        resp = client.describe_db_clusters(Marker=marker)
        clusters.extend(resp['DBClusters'])
        marker = resp.get('Marker', None)
    account_id = boto.connect_iam().get_user().arn.split(':')[4]
    c_dict = {
        
    }
    for c in clusters:
        if (not self.ec2_instance_filters):
            matches_filter = True
        else:
            matches_filter = False
        try:
            tags = client.list_tags_for_resource(ResourceName=((((('arn:aws:rds:' + region) + ':') + account_id) + ':cluster:') + c['DBClusterIdentifier']))
            c['Tags'] = tags['TagList']
            if self.ec2_instance_filters:
                for filters in self.ec2_instance_filters:
                    for (filter_key, filter_values) in filters.items():
                        tag_name = filter_key.split(':', 1)[1]
                        matches_filter = any((((d['Key'] == tag_name) and (d['Value'] in filter_values)) for d in c['Tags']))
                        if matches_filter:
                            break
                    if matches_filter:
                        break
        except Exception as e:
            if (e.message.find('DBInstanceNotFound') >= 0):
                pass
        if (len(c['DBClusterMembers']) == 0):
            continue
        elif matches_filter:
            c_dict[c['DBClusterIdentifier']] = c
    self.inventory['db_clusters'] = c_dict