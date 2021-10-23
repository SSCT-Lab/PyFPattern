

def converge_file_system(self, name, tags, targets):
    '\n         Change attributes (mount targets and tags) of filesystem by name\n        '
    result = False
    fs_id = self.get_file_system_id(name)
    if (tags is not None):
        (tags_to_create, _, tags_to_delete) = dict_diff(self.get_tags(FileSystemId=fs_id), tags)
        if tags_to_delete:
            self.connection.delete_tags(FileSystemId=fs_id, TagKeys=[item[0] for item in tags_to_delete])
            result = True
        if tags_to_create:
            self.connection.create_tags(FileSystemId=fs_id, Tags=[{
                'Key': item[0],
                'Value': item[1],
            } for item in tags_to_create])
            result = True
    if (targets is not None):
        incomplete_states = [self.STATE_CREATING, self.STATE_DELETING]
        wait_for((lambda : len(self.get_mount_targets_in_state(fs_id, incomplete_states))), 0)
        index_by_subnet_id = (lambda items: dict(((item['SubnetId'], item) for item in items)))
        current_targets = index_by_subnet_id(self.get_mount_targets(FileSystemId=fs_id))
        targets = index_by_subnet_id(targets)
        (targets_to_create, intersection, targets_to_delete) = dict_diff(current_targets, targets, True)
        changed = [sid for sid in intersection if (not targets_equal(['SubnetId', 'IpAddress', 'NetworkInterfaceId'], current_targets[sid], targets[sid]))]
        targets_to_delete = (list(targets_to_delete) + changed)
        targets_to_create = (list(targets_to_create) + changed)
        if targets_to_delete:
            for sid in targets_to_delete:
                self.connection.delete_mount_target(MountTargetId=current_targets[sid]['MountTargetId'])
            wait_for((lambda : len(self.get_mount_targets_in_state(fs_id, incomplete_states))), 0)
            result = True
        if targets_to_create:
            for sid in targets_to_create:
                self.connection.create_mount_target(FileSystemId=fs_id, **targets[sid])
            wait_for((lambda : len(self.get_mount_targets_in_state(fs_id, incomplete_states))), 0, self.wait_timeout)
            result = True
        security_groups_to_update = [sid for sid in intersection if (('SecurityGroups' in targets[sid]) and (current_targets[sid]['SecurityGroups'] != targets[sid]['SecurityGroups']))]
        if security_groups_to_update:
            for sid in security_groups_to_update:
                self.connection.modify_mount_target_security_groups(MountTargetId=current_targets[sid]['MountTargetId'], SecurityGroups=targets[sid].get('SecurityGroups', None))
            result = True
    return result
