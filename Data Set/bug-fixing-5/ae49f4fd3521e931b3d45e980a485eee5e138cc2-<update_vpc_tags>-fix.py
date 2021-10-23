def update_vpc_tags(connection, module, vpc_id, tags, name):
    if (tags is None):
        tags = dict()
    tags.update({
        'Name': name,
    })
    tags = dict(((k, to_native(v)) for (k, v) in tags.items()))
    try:
        current_tags = dict(((t['Key'], t['Value']) for t in connection.describe_tags(Filters=[{
            'Name': 'resource-id',
            'Values': [vpc_id],
        }])['Tags']))
        (tags_to_update, dummy) = compare_aws_tags(current_tags, tags, False)
        if tags_to_update:
            if (not module.check_mode):
                tags = ansible_dict_to_boto3_tag_list(tags_to_update)
                vpc_obj = AWSRetry.backoff(delay=1, tries=5, catch_extra_error_codes=['InvalidVpcID.NotFound'])(connection.create_tags)(Resources=[vpc_id], Tags=tags)
                expected_tags = boto3_tag_list_to_ansible_dict(tags)
                filters = [{
                    'Name': 'tag:{0}'.format(key),
                    'Values': [value],
                } for (key, value) in expected_tags.items()]
                connection.get_waiter('vpc_available').wait(VpcIds=[vpc_id], Filters=filters)
            return True
        else:
            return False
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, msg='Failed to update tags')