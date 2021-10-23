@AWSRetry.exponential_backoff()
def get_mount_targets(self, file_system_id):
    '\n         Returns mount targets for selected instance of EFS\n        '
    paginator = self.connection.get_paginator('describe_mount_targets')
    return paginator.paginate(FileSystemId=file_system_id).build_full_result()['MountTargets']