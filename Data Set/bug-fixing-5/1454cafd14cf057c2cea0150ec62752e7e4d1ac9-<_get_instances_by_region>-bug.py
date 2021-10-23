def _get_instances_by_region(self, regions, filters, strict_permissions):
    '\n           :param regions: a list of regions in which to describe instances\n           :param filters: a list of boto3 filter dicionaries\n           :param strict_permissions: a boolean determining whether to fail or ignore 403 error codes\n           :return A list of namedtuples containing the fields region, instance_meta, and instance_data\n        '
    all_instances = []
    for (connection, region) in self._boto3_conn(regions):
        try:
            paginator = connection.get_paginator('describe_instances')
            reservations = paginator.paginate(Filters=filters).build_full_result().get('Reservations')
            instances = []
            for r in reservations:
                instances.extend(r.get('Instances'))
        except botocore.exceptions.ClientError as e:
            if ((e.response['ResponseMetadata']['HTTPStatusCode'] == 403) and (not strict_permissions)):
                instances = []
            else:
                raise AnsibleError(('Failed to describe instances: %s' % to_native(e)))
        except botocore.exceptions.BotoCoreError as e:
            raise AnsibleError(('Failed to describe instances: %s' % to_native(e)))
        all_instances.extend(instances)
    return sorted(all_instances, key=(lambda x: x['InstanceId']))