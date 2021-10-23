def list_ec2_images(ec2_client, module):
    image_ids = module.params.get('image_ids')
    owners = module.params.get('owners')
    executable_users = module.params.get('executable_users')
    filters = module.params.get('filters')
    owner_param = []
    for owner in owners:
        if owner.isdigit():
            if ('owner-id' not in filters):
                filters['owner-id'] = list()
            filters['owner-id'].append(owner)
        elif (owner == 'self'):
            owner_param.append(owner)
        else:
            if ('owner-alias' not in filters):
                filters['owner-alias'] = list()
            filters['owner-alias'].append(owner)
    filters = ansible_dict_to_boto3_filter_list(filters)
    try:
        images = ec2_client.describe_images(ImageIds=image_ids, Filters=filters, Owners=owner_param, ExecutableUsers=executable_users)
        images = [camel_dict_to_snake_dict(image) for image in images['Images']]
    except (ClientError, BotoCoreError) as err:
        module.fail_json_aws(err, msg='error describing images')
    for image in images:
        try:
            image['tags'] = boto3_tag_list_to_ansible_dict(image.get('tags', []))
            if module.params.get('describe_image_attributes'):
                launch_permissions = ec2_client.describe_image_attribute(Attribute='launchPermission', ImageId=image['image_id'])['LaunchPermissions']
                image['launch_permissions'] = [camel_dict_to_snake_dict(perm) for perm in launch_permissions]
        except (ClientError, BotoCoreError) as err:
            pass
    module.exit_json(images=images)