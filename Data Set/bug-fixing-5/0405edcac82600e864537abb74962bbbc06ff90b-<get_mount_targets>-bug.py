def get_mount_targets(self, **kwargs):
    '\n         Returns mount targets for selected instance of EFS\n        '
    targets = iterate_all('MountTargets', self.connection.describe_mount_targets, **kwargs)
    for target in targets:
        if (target['LifeCycleState'] == self.STATE_AVAILABLE):
            target['SecurityGroups'] = list(self.get_security_groups(MountTargetId=target['MountTargetId']))
        else:
            target['SecurityGroups'] = []
        (yield target)