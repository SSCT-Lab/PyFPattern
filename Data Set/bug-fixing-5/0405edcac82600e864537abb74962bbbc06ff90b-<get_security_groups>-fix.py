@AWSRetry.exponential_backoff()
def get_security_groups(self, mount_target_id):
    '\n         Returns security groups for selected instance of EFS\n        '
    return self.connection.describe_mount_target_security_groups(MountTargetId=mount_target_id)['SecurityGroups']