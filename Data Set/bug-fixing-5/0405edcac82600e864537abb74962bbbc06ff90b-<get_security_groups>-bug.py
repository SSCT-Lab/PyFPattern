def get_security_groups(self, **kwargs):
    '\n         Returns security groups for selected instance of EFS\n        '
    return iterate_all('SecurityGroups', self.connection.describe_mount_target_security_groups, **kwargs)