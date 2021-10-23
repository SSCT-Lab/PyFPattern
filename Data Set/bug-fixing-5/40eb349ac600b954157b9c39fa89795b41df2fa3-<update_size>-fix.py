def update_size(connection, group, max_size, min_size, dc):
    log.debug('setting ASG sizes')
    log.debug('minimum size: {0}, desired_capacity: {1}, max size: {2}'.format(min_size, dc, max_size))
    updated_group = dict()
    updated_group['AutoScalingGroupName'] = group['AutoScalingGroupName']
    updated_group['MinSize'] = min_size
    updated_group['MaxSize'] = max_size
    updated_group['DesiredCapacity'] = dc
    update_asg(connection, **updated_group)