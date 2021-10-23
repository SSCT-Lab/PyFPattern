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
        for reservation in reservations:
            for instance in reservation.instances:
                self.add_instance(instance, region)
    except boto.exception.BotoServerError as e:
        if (e.error_code == 'AuthFailure'):
            error = self.get_auth_error_message()
        else:
            backend = ('Eucalyptus' if self.eucalyptus else 'AWS')
            error = ('Error connecting to %s backend.\n%s' % (backend, e.message))
        self.fail_with_error(error, 'getting EC2 instances')