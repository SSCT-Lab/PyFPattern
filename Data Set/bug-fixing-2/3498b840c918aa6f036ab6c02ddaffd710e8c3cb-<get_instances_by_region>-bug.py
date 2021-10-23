

def get_instances_by_region(self, region):
    ' Makes an AWS EC2 API call to the list of instances in a particular\n        region '
    try:
        conn = self.connect(region)
        reservations = []
        if self.ec2_instance_filters:
            for (filter_key, filter_values) in self.ec2_instance_filters.items():
                reservations.extend(conn.get_all_instances(filters={
                    filter_key: filter_values,
                }))
        else:
            reservations = conn.get_all_instances()
        instance_ids = []
        for reservation in reservations:
            instance_ids.extend([instance.id for instance in reservation.instances])
        tags = conn.get_all_tags(filters={
            'resource-type': 'instance',
            'resource-id': instance_ids,
        })
        tags_by_instance_id = defaultdict(dict)
        for tag in tags:
            tags_by_instance_id[tag.res_id][tag.name] = tag.value
        for reservation in reservations:
            for instance in reservation.instances:
                instance.tags = tags_by_instance_id[instance.id]
                self.add_instance(instance, region)
    except boto.exception.BotoServerError as e:
        if (e.error_code == 'AuthFailure'):
            error = self.get_auth_error_message()
        else:
            backend = ('Eucalyptus' if self.eucalyptus else 'AWS')
            error = ('Error connecting to %s backend.\n%s' % (backend, e.message))
        self.fail_with_error(error, 'getting EC2 instances')
