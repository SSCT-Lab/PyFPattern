def get_file_systems(self, **kwargs):
    '\n         Returns generator of file systems including all attributes of FS\n        '
    items = iterate_all('FileSystems', self.connection.describe_file_systems, **kwargs)
    for item in items:
        item['Name'] = item['CreationToken']
        item['CreationTime'] = str(item['CreationTime'])
        '\n            Suffix of network path to be used as NFS device for mount. More detail here:\n            http://docs.aws.amazon.com/efs/latest/ug/gs-step-three-connect-to-ec2-instance.html\n            '
        item['MountPoint'] = ('.%s.efs.%s.amazonaws.com:/' % (item['FileSystemId'], self.region))
        if ('Timestamp' in item['SizeInBytes']):
            item['SizeInBytes']['Timestamp'] = str(item['SizeInBytes']['Timestamp'])
        if (item['LifeCycleState'] == self.STATE_AVAILABLE):
            item['Tags'] = self.get_tags(FileSystemId=item['FileSystemId'])
            item['MountTargets'] = list(self.get_mount_targets(FileSystemId=item['FileSystemId']))
        else:
            item['Tags'] = {
                
            }
            item['MountTargets'] = []
        (yield item)