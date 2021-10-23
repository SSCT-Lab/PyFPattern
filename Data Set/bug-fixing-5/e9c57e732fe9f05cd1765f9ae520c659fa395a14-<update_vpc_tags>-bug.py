def update_vpc_tags(connection, module, vpc_id, tags, name):
    if (tags is None):
        tags = dict()
    tags.update({
        'Name': name,
    })
    try:
        current_tags = dict(((t['Key'], t['Value']) for t in connection.describe_tags(Filters=[{
            'Name': 'resource-id',
            'Values': [vpc_id],
        }])['Tags']))
        if (tags != current_tags):
            if (not module.check_mode):
                tags = ansible_dict_to_boto3_tag_list(tags)
                connection.create_tags(Resources=[vpc_id], Tags=tags)
            return True
        else:
            return False
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, msg='Failed to update tags')