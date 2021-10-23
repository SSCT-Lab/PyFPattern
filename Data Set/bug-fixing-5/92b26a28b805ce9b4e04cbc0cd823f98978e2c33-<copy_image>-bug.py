def copy_image(module, ec2):
    '\n    Copies an AMI\n\n    module : AnsibleModule object\n    ec2: authenticated ec2 connection object\n    '
    source_region = module.params.get('source_region')
    source_image_id = module.params.get('source_image_id')
    name = module.params.get('name')
    description = module.params.get('description')
    encrypted = module.params.get('encrypted')
    kms_key_id = module.params.get('kms_key_id')
    tags = module.params.get('tags')
    wait_timeout = int(module.params.get('wait_timeout'))
    wait = module.params.get('wait')
    try:
        params = {
            'source_region': source_region,
            'source_image_id': source_image_id,
            'name': name,
            'description': description,
            'encrypted': encrypted,
            'kms_key_id': kms_key_id,
        }
        image_id = ec2.copy_image(**params).image_id
    except boto.exception.BotoServerError as e:
        module.fail_json(msg=('%s: %s' % (e.error_code, e.error_message)))
    img = wait_until_image_is_recognized(module, ec2, wait_timeout, image_id, wait)
    img = wait_until_image_is_copied(module, ec2, wait_timeout, img, image_id, wait)
    register_tags_if_any(module, ec2, tags, image_id)
    module.exit_json(msg='AMI copy operation complete', image_id=image_id, state=img.state, changed=True)