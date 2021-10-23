def tags_action(client, stream_name, tags, action='create', check_mode=False):
    'Create or delete multiple tags from a Kinesis Stream.\n    Args:\n        client (botocore.client.EC2): Boto3 client.\n        resource_id (str): The Amazon resource id.\n        tags (list): List of dictionaries.\n            examples.. [{Name: "", Values: [""]}]\n\n    Kwargs:\n        action (str): The action to perform.\n            valid actions == create and delete\n            default=create\n        check_mode (bool): This will pass DryRun as one of the parameters to the aws api.\n            default=False\n\n    Basic Usage:\n        >>> client = boto3.client(\'ec2\')\n        >>> resource_id = \'pcx-123345678\'\n        >>> tags = {\'env\': \'development\'}\n        >>> update_tags(client, resource_id, tags)\n        [True, \'\']\n\n    Returns:\n        List (bool, str)\n    '
    success = False
    err_msg = ''
    params = {
        'StreamName': stream_name,
    }
    try:
        if (not check_mode):
            if (action == 'create'):
                params['Tags'] = tags
                client.add_tags_to_stream(**params)
                success = True
            elif (action == 'delete'):
                params['TagKeys'] = tags.keys()
                client.remove_tags_from_stream(**params)
                success = True
            else:
                err_msg = 'Invalid action {0}'.format(action)
        elif (action == 'create'):
            success = True
        elif (action == 'delete'):
            success = True
        else:
            err_msg = 'Invalid action {0}'.format(action)
    except botocore.exceptions.ClientError as e:
        err_msg = to_native(e)
    return (success, err_msg)