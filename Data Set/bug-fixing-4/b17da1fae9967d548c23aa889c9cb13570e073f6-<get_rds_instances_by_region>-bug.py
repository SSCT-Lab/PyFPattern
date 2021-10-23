def get_rds_instances_by_region(self, region):
    ' Makes an AWS API call to the list of RDS instances in a particular\n        region '
    if (not HAS_BOTO3):
        self.fail_with_error('Working with RDS instances requires boto3 - please install boto3 and try again', 'getting RDS instances')
    client = ec2_utils.boto3_inventory_conn('client', 'rds', region, **self.credentials)
    db_instances = client.describe_db_instances()
    try:
        conn = self.connect_to_aws(rds, region)
        if conn:
            marker = None
            while True:
                instances = conn.get_all_dbinstances(marker=marker)
                marker = instances.marker
                for (index, instance) in enumerate(instances):
                    instance.arn = db_instances['DBInstances'][index]['DBInstanceArn']
                    tags = client.list_tags_for_resource(ResourceName=instance.arn)['TagList']
                    instance.tags = {
                        
                    }
                    for tag in tags:
                        instance.tags[tag['Key']] = tag['Value']
                    self.add_rds_instance(instance, region)
                if (not marker):
                    break
    except boto.exception.BotoServerError as e:
        error = e.reason
        if (e.error_code == 'AuthFailure'):
            error = self.get_auth_error_message()
        if (not (e.reason == 'Forbidden')):
            error = ('Looks like AWS RDS is down:\n%s' % e.message)
        self.fail_with_error(error, 'getting RDS instances')