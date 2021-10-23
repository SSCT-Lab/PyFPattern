

def list_ec2_images(ec2_client, module):
    image_ids = module.params.get('image_ids')
    filters = ansible_dict_to_boto3_filter_list(module.params.get('filters'))
    owners = module.params.get('owners')
    executable_users = module.params.get('executable_users')
    try:
        images = ec2_client.describe_images(ImageIds=image_ids, Filters=filters, Owners=owners, ExecutableUsers=executable_users)
        images = [camel_dict_to_snake_dict(image) for image in images['Images']]
        for image in images:
            launch_permissions = ec2_client.describe_image_attribute(Attribute='launchPermission', ImageId=image['image_id'])['LaunchPermissions']
            image['launch_permissions'] = [camel_dict_to_snake_dict(perm) for perm in launch_permissions]
    except (ClientError, BotoCoreError) as err:
        module.fail_json_aws(err, msg='error describing images')
    for image in images:
        image['tags'] = boto3_tag_list_to_ansible_dict(image.get('tags', []), 'key', 'value')
    module.exit_json(images=images)
