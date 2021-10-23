

def create_launch_config(connection, module):
    name = module.params.get('name')
    vpc_id = module.params.get('vpc_id')
    try:
        (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
        ec2_connection = boto3_conn(module, 'client', 'ec2', region, ec2_url, **aws_connect_kwargs)
        security_groups = get_ec2_security_group_ids_from_names(module.params.get('security_groups'), ec2_connection, vpc_id=vpc_id, boto3=True)
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg='Failed to get Security Group IDs', exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    except ValueError as e:
        module.fail_json(msg='Failed to get Security Group IDs', exception=traceback.format_exc())
    user_data = module.params.get('user_data')
    user_data_path = module.params.get('user_data_path')
    volumes = module.params['volumes']
    instance_monitoring = module.params.get('instance_monitoring')
    assign_public_ip = module.params.get('assign_public_ip')
    instance_profile_name = module.params.get('instance_profile_name')
    ebs_optimized = module.params.get('ebs_optimized')
    classic_link_vpc_id = module.params.get('classic_link_vpc_id')
    classic_link_vpc_security_groups = module.params.get('classic_link_vpc_security_groups')
    block_device_mapping = []
    convert_list = ['image_id', 'instance_type', 'instance_type', 'instance_id', 'placement_tenancy', 'key_name', 'kernel_id', 'ramdisk_id', 'spot_price']
    launch_config = snake_dict_to_camel_dict(dict(((k.capitalize(), str(v)) for (k, v) in module.params.items() if ((v is not None) and (k in convert_list)))))
    if user_data_path:
        try:
            with open(user_data_path, 'r') as user_data_file:
                user_data = user_data_file.read()
        except IOError as e:
            module.fail_json(msg='Failed to open file for reading', exception=traceback.format_exc())
    if volumes:
        for volume in volumes:
            if ('device_name' not in volume):
                module.fail_json(msg='Device name must be set for volume')
            if (('volume_size' not in volume) or (int(volume['volume_size']) > 0)):
                block_device_mapping.append(create_block_device_meta(module, volume))
    try:
        launch_configs = connection.describe_launch_configurations(LaunchConfigurationNames=[name]).get('LaunchConfigurations')
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg='Failed to describe launch configuration by name', exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    changed = False
    result = {
        
    }
    launch_config['LaunchConfigurationName'] = name
    if (security_groups is not None):
        launch_config['SecurityGroups'] = security_groups
    if (classic_link_vpc_id is not None):
        launch_config['ClassicLinkVPCId'] = classic_link_vpc_id
    if (instance_monitoring is not None):
        launch_config['InstanceMonitoring'] = {
            'Enabled': instance_monitoring,
        }
    if (classic_link_vpc_security_groups is not None):
        launch_config['ClassicLinkVPCSecurityGroups'] = classic_link_vpc_security_groups
    if block_device_mapping:
        launch_config['BlockDeviceMappings'] = block_device_mapping
    if (instance_profile_name is not None):
        launch_config['IamInstanceProfile'] = instance_profile_name
    if (assign_public_ip is not None):
        launch_config['AssociatePublicIpAddress'] = assign_public_ip
    if (user_data is not None):
        launch_config['UserData'] = user_data
    if (ebs_optimized is not None):
        launch_config['EbsOptimized'] = ebs_optimized
    if (len(launch_configs) == 0):
        try:
            connection.create_launch_configuration(**launch_config)
            launch_configs = connection.describe_launch_configurations(LaunchConfigurationNames=[name]).get('LaunchConfigurations')
            changed = True
            if launch_configs:
                launch_config = launch_configs[0]
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg='Failed to create launch configuration', exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    result = dict(((k, v) for (k, v) in launch_config.items() if (k not in ['Connection', 'CreatedTime', 'InstanceMonitoring', 'BlockDeviceMappings'])))
    result['CreatedTime'] = to_text(launch_config.get('CreatedTime'))
    try:
        result['InstanceMonitoring'] = module.boolean(launch_config.get('InstanceMonitoring').get('Enabled'))
    except AttributeError:
        result['InstanceMonitoring'] = False
    result['BlockDeviceMappings'] = []
    for block_device_mapping in launch_config.get('BlockDeviceMappings', []):
        result['BlockDeviceMappings'].append(dict(device_name=block_device_mapping.get('DeviceName'), virtual_name=block_device_mapping.get('VirtualName')))
        if (block_device_mapping.get('Ebs') is not None):
            result['BlockDeviceMappings'][(- 1)]['ebs'] = dict(snapshot_id=block_device_mapping.get('Ebs').get('SnapshotId'), volume_size=block_device_mapping.get('Ebs').get('VolumeSize'))
    if user_data_path:
        result['UserData'] = 'hidden'
    return_object = {
        'Name': result.get('LaunchConfigurationName'),
        'CreatedTime': result.get('CreatedTime'),
        'ImageId': result.get('ImageId'),
        'Arn': result.get('LaunchConfigurationARN'),
        'SecurityGroups': result.get('SecurityGroups'),
        'InstanceType': result.get('InstanceType'),
        'Result': result,
    }
    module.exit_json(changed=changed, **camel_dict_to_snake_dict(return_object))
