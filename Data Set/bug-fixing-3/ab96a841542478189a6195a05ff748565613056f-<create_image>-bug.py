def create_image(module, connection):
    instance_id = module.params.get('instance_id')
    name = module.params.get('name')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    description = module.params.get('description')
    architecture = module.params.get('architecture')
    kernel_id = module.params.get('kernel_id')
    root_device_name = module.params.get('root_device_name')
    virtualization_type = module.params.get('virtualization_type')
    no_reboot = module.params.get('no_reboot')
    device_mapping = module.params.get('device_mapping')
    tags = module.params.get('tags')
    launch_permissions = module.params.get('launch_permissions')
    image_location = module.params.get('image_location')
    enhanced_networking = module.params.get('enhanced_networking')
    billing_products = module.params.get('billing_products')
    ramdisk_id = module.params.get('ramdisk_id')
    sriov_net_support = module.params.get('sriov_net_support')
    try:
        params = {
            'Name': name,
            'Description': description,
        }
        block_device_mapping = None
        if device_mapping:
            block_device_mapping = []
            for device in device_mapping:
                device['Ebs'] = {
                    
                }
                if ('device_name' not in device):
                    module.fail_json(msg='Error - Device name must be set for volume.')
                device = rename_item_if_exists(device, 'device_name', 'DeviceName')
                device = rename_item_if_exists(device, 'virtual_name', 'VirtualName')
                device = rename_item_if_exists(device, 'no_device', 'NoDevice')
                device = rename_item_if_exists(device, 'volume_type', 'VolumeType', 'Ebs')
                device = rename_item_if_exists(device, 'snapshot_id', 'SnapshotId', 'Ebs')
                device = rename_item_if_exists(device, 'delete_on_termination', 'DeleteOnTermination', 'Ebs')
                device = rename_item_if_exists(device, 'size', 'VolumeSize', 'Ebs')
                device = rename_item_if_exists(device, 'volume_size', 'VolumeSize', 'Ebs')
                device = rename_item_if_exists(device, 'iops', 'Iops', 'Ebs')
                device = rename_item_if_exists(device, 'encrypted', 'Encrypted', 'Ebs')
                block_device_mapping.append(device)
        if block_device_mapping:
            params['BlockDeviceMappings'] = block_device_mapping
        if instance_id:
            params['InstanceId'] = instance_id
            params['NoReboot'] = no_reboot
            image_id = connection.create_image(**params).get('ImageId')
        else:
            if architecture:
                params['Architecture'] = architecture
            if virtualization_type:
                params['VirtualizationType'] = virtualization_type
            if image_location:
                params['ImageLocation'] = image_location
            if enhanced_networking:
                params['EnaSupport'] = enhanced_networking
            if billing_products:
                params['BillingProducts'] = billing_products
            if ramdisk_id:
                params['RamdiskId'] = ramdisk_id
            if sriov_net_support:
                params['SriovNetSupport'] = sriov_net_support
            if kernel_id:
                params['KernelId'] = kernel_id
            if root_device_name:
                params['RootDeviceName'] = root_device_name
            image_id = connection.register_image(**params).get('ImageId')
    except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
        module.fail_json_aws(e, msg='Error registering image')
    if wait:
        waiter = connection.get_waiter('image_available')
        delay = (wait_timeout // 30)
        max_attempts = 30
        waiter.wait(ImageIds=[image_id], WaiterConfig=dict(Delay=delay, MaxAttempts=max_attempts))
    if tags:
        try:
            connection.create_tags(Resources=[image_id], Tags=ansible_dict_to_boto3_tag_list(tags))
        except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
            module.fail_json_aws(e, msg='Error tagging image')
    if launch_permissions:
        try:
            params = dict(Attribute='LaunchPermission', ImageId=image_id, LaunchPermission=dict(Add=list()))
            for group_name in launch_permissions.get('group_names', []):
                params['LaunchPermission']['Add'].append(dict(Group=group_name))
            for user_id in launch_permissions.get('user_ids', []):
                params['LaunchPermission']['Add'].append(dict(UserId=str(user_id)))
            if params['LaunchPermission']['Add']:
                connection.modify_image_attribute(**params)
        except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
            module.fail_json_aws(e, msg=('Error setting launch permissions for image %s' % image_id))
    module.exit_json(msg='AMI creation operation complete.', changed=True, **get_ami_info(get_image_by_id(module, connection, image_id)))