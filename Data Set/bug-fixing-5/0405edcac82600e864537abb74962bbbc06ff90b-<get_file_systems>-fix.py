def get_file_systems(self, file_system_id=None, creation_token=None):
    kwargs = dict()
    if file_system_id:
        kwargs['FileSystemId'] = file_system_id
    if creation_token:
        kwargs['CreationToken'] = creation_token
    try:
        file_systems = self.list_file_systems(**kwargs)
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        self.module.fail_json_aws(e, msg="Couldn't get EFS file systems")
    results = list()
    for item in file_systems:
        item['CreationTime'] = str(item['CreationTime'])
        '\n            Suffix of network path to be used as NFS device for mount. More detail here:\n            http://docs.aws.amazon.com/efs/latest/ug/gs-step-three-connect-to-ec2-instance.html\n            '
        item['MountPoint'] = ('.%s.efs.%s.amazonaws.com:/' % (item['FileSystemId'], self.region))
        if ('Timestamp' in item['SizeInBytes']):
            item['SizeInBytes']['Timestamp'] = str(item['SizeInBytes']['Timestamp'])
        if (item['LifeCycleState'] == self.STATE_AVAILABLE):
            try:
                item['MountTargets'] = self.get_mount_targets(item['FileSystemId'])
            except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                self.module.fail_json_aws(e, msg="Couldn't get EFS targets")
            for target in item['MountTargets']:
                if (target['LifeCycleState'] == self.STATE_AVAILABLE):
                    try:
                        target['SecurityGroups'] = self.get_security_groups(target['MountTargetId'])
                    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                        self.module.fail_json_aws(e, msg="Couldn't get EFS security groups")
                else:
                    target['SecurityGroups'] = []
        else:
            item['tags'] = {
                
            }
            item['mount_targets'] = []
        result = camel_dict_to_snake_dict(item)
        if (result['life_cycle_state'] == self.STATE_AVAILABLE):
            try:
                result['tags'] = self.get_tags(result['file_system_id'])
            except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                self.module.fail_json_aws(e, msg="Couldn't get EFS tags")
        results.append(result)
    return results