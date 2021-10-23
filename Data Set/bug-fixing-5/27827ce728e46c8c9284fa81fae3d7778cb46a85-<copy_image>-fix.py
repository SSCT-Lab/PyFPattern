def copy_image(module, ec2):
    '\n    Copies an AMI\n\n    module : AnsibleModule object\n    ec2: ec2 connection object\n    '
    image = None
    changed = False
    tags = module.params.get('tags')
    params = {
        'SourceRegion': module.params.get('source_region'),
        'SourceImageId': module.params.get('source_image_id'),
        'Name': module.params.get('name'),
        'Description': module.params.get('description'),
        'Encrypted': module.params.get('encrypted'),
    }
    if module.params.get('kms_key_id'):
        params['KmsKeyId'] = module.params.get('kms_key_id')
    try:
        if module.params.get('tag_equality'):
            filters = [{
                'Name': ('tag:%s' % k),
                'Values': [v],
            } for (k, v) in module.params.get('tags').items()]
            filters.append(dict(Name='state', Values=['available', 'pending']))
            images = ec2.describe_images(Filters=filters)
            if (len(images['Images']) > 0):
                image = images['Images'][0]
        if (not image):
            image = ec2.copy_image(**params)
            image_id = image['ImageId']
            if tags:
                ec2.create_tags(Resources=[image_id], Tags=ansible_dict_to_boto3_tag_list(tags))
            changed = True
        if module.params.get('wait'):
            delay = 15
            max_attempts = (module.params.get('wait_timeout') // delay)
            image_id = image.get('ImageId')
            ec2.get_waiter('image_available').wait(ImageIds=[image_id], WaiterConfig={
                'Delay': delay,
                'MaxAttempts': max_attempts,
            })
        module.exit_json(changed=changed, **camel_dict_to_snake_dict(image))
    except WaiterError as e:
        module.fail_json_aws(e, msg='An error occurred waiting for the image to become available')
    except (ClientError, BotoCoreError) as e:
        module.fail_json_aws(e, msg='Could not copy AMI')
    except Exception as e:
        module.fail_json(msg=('Unhandled exception. (%s)' % to_native(e)))