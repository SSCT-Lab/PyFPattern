def create_stream(client, stream_name, number_of_shards=1, retention_period=None, tags=None, wait=False, wait_timeout=300, check_mode=False):
    "Create an Amazon Kinesis Stream.\n    Args:\n        client (botocore.client.EC2): Boto3 client.\n        stream_name (str): The name of the kinesis stream.\n\n    Kwargs:\n        number_of_shards (int): Number of shards this stream will use.\n            default=1\n        retention_period (int): Can not be less than 24 hours\n            default=None\n        tags (dict): The tags you want applied.\n            default=None\n        wait (bool): Wait until Stream is ACTIVE.\n            default=False\n        wait_timeout (int): How long to wait until this operation is considered failed.\n            default=300\n        check_mode (bool): This will pass DryRun as one of the parameters to the aws api.\n            default=False\n\n    Basic Usage:\n        >>> client = boto3.client('kinesis')\n        >>> stream_name = 'test-stream'\n        >>> number_of_shards = 10\n        >>> tags = {'env': 'test'}\n        >>> create_stream(client, stream_name, number_of_shards, tags=tags)\n\n    Returns:\n        Tuple (bool, bool, str, dict)\n    "
    success = False
    changed = False
    err_msg = ''
    results = dict()
    (stream_found, stream_msg, current_stream) = find_stream(client, stream_name, check_mode=check_mode)
    if (stream_found and (current_stream.get('StreamStatus') == 'DELETING') and wait):
        (wait_success, wait_msg, current_stream) = wait_for_status(client, stream_name, 'ACTIVE', wait_timeout, check_mode=check_mode)
    if (stream_found and (not check_mode)):
        if (current_stream['ShardsCount'] != number_of_shards):
            err_msg = 'Can not change the number of shards in a Kinesis Stream'
            return (success, changed, err_msg, results)
    if (stream_found and (current_stream.get('StreamStatus') != 'DELETING')):
        (success, changed, err_msg) = update(client, current_stream, stream_name, number_of_shards, retention_period, tags, wait, wait_timeout, check_mode=check_mode)
    else:
        (create_success, create_msg) = stream_action(client, stream_name, number_of_shards, action='create', check_mode=check_mode)
        if (not create_success):
            changed = True
            err_msg = 'Failed to create Kinesis stream: {0}'.format(create_msg)
            return (False, True, err_msg, {
                
            })
        else:
            changed = True
            if wait:
                (wait_success, wait_msg, results) = wait_for_status(client, stream_name, 'ACTIVE', wait_timeout, check_mode=check_mode)
                err_msg = 'Kinesis Stream {0} is in the process of being created'.format(stream_name)
                if (not wait_success):
                    return (wait_success, True, wait_msg, results)
            else:
                err_msg = 'Kinesis Stream {0} created successfully'.format(stream_name)
            if tags:
                (changed, err_msg) = tags_action(client, stream_name, tags, action='create', check_mode=check_mode)
                if changed:
                    success = True
                if (not success):
                    return (success, changed, err_msg, results)
            (stream_found, stream_msg, current_stream) = find_stream(client, stream_name, check_mode=check_mode)
            if (retention_period and (current_stream.get('StreamStatus') == 'ACTIVE')):
                (changed, err_msg) = retention_action(client, stream_name, retention_period, action='increase', check_mode=check_mode)
                if changed:
                    success = True
                if (not success):
                    return (success, changed, err_msg, results)
            else:
                err_msg = 'StreamStatus has to be ACTIVE in order to modify the retention period. Current status is {0}'.format(current_stream.get('StreamStatus', 'UNKNOWN'))
                success = create_success
                changed = True
    if success:
        (_, _, results) = find_stream(client, stream_name, check_mode=check_mode)
        (_, _, current_tags) = get_tags(client, stream_name, check_mode=check_mode)
        if (current_tags and (not check_mode)):
            current_tags = make_tags_in_proper_format(current_tags)
            results['Tags'] = current_tags
        elif (check_mode and tags):
            results['Tags'] = tags
        else:
            results['Tags'] = dict()
        results = convert_to_lower(results)
    return (success, changed, err_msg, results)