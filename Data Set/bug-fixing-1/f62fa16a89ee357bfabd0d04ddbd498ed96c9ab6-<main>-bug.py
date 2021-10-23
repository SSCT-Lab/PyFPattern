

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(name=dict(type='str', required=True), state=dict(type='str', default='present', choices=['present', 'absent']), runtime=dict(type='str', required=True), role=dict(type='str', default=None), handler=dict(type='str', default=None), zip_file=dict(type='str', default=None, aliases=['src']), s3_bucket=dict(type='str'), s3_key=dict(type='str'), s3_object_version=dict(type='str', default=None), description=dict(type='str', default=''), timeout=dict(type='int', default=3), memory_size=dict(type='int', default=128), vpc_subnet_ids=dict(type='list', default=None), vpc_security_group_ids=dict(type='list', default=None), environment_variables=dict(type='dict', default=None), dead_letter_arn=dict(type='str', default=None)))
    mutually_exclusive = [['zip_file', 's3_key'], ['zip_file', 's3_bucket'], ['zip_file', 's3_object_version']]
    required_together = [['s3_key', 's3_bucket'], ['vpc_subnet_ids', 'vpc_security_group_ids']]
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, mutually_exclusive=mutually_exclusive, required_together=required_together)
    name = module.params.get('name')
    state = module.params.get('state').lower()
    runtime = module.params.get('runtime')
    role = module.params.get('role')
    handler = module.params.get('handler')
    s3_bucket = module.params.get('s3_bucket')
    s3_key = module.params.get('s3_key')
    s3_object_version = module.params.get('s3_object_version')
    zip_file = module.params.get('zip_file')
    description = module.params.get('description')
    timeout = module.params.get('timeout')
    memory_size = module.params.get('memory_size')
    vpc_subnet_ids = module.params.get('vpc_subnet_ids')
    vpc_security_group_ids = module.params.get('vpc_security_group_ids')
    environment_variables = module.params.get('environment_variables')
    dead_letter_arn = module.params.get('dead_letter_arn')
    check_mode = module.check_mode
    changed = False
    if (not HAS_BOTOCORE):
        module.fail_json(msg='Python module "botocore" is missing, please install it')
    if (not HAS_BOTO3):
        module.fail_json(msg='Python module "boto3" is missing, please install it')
    (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
    if (not region):
        module.fail_json(msg='region must be specified')
    try:
        client = boto3_conn(module, conn_type='client', resource='lambda', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except (botocore.exceptions.ClientError, botocore.exceptions.ValidationError) as e:
        module.fail_json(msg=str(e))
    if role.startswith('arn:aws:iam'):
        role_arn = role
    else:
        try:
            iam_client = boto3_conn(module, conn_type='client', resource='iam', region=region, endpoint=ec2_url, **aws_connect_kwargs)
            account_id = iam_client.get_user()['User']['Arn'].split(':')[4]
            role_arn = 'arn:aws:iam::{0}:role/{1}'.format(account_id, role)
        except (botocore.exceptions.ClientError, botocore.exceptions.ValidationError) as e:
            module.fail_json(msg=str(e))
    current_function = get_current_function(client, name)
    if ((state == 'present') and current_function):
        current_config = current_function['Configuration']
        current_version = None
        func_kwargs = {
            'FunctionName': name,
        }
        if (role_arn and (current_config['Role'] != role_arn)):
            func_kwargs.update({
                'Role': role_arn,
            })
        if (handler and (current_config['Handler'] != handler)):
            func_kwargs.update({
                'Handler': handler,
            })
        if (description and (current_config['Description'] != description)):
            func_kwargs.update({
                'Description': description,
            })
        if (timeout and (current_config['Timeout'] != timeout)):
            func_kwargs.update({
                'Timeout': timeout,
            })
        if (memory_size and (current_config['MemorySize'] != memory_size)):
            func_kwargs.update({
                'MemorySize': memory_size,
            })
        if ((environment_variables is not None) and (current_config.get('Environment', {
            
        }).get('Variables', {
            
        }) != environment_variables)):
            func_kwargs.update({
                'Environment': {
                    'Variables': environment_variables,
                },
            })
        if (dead_letter_arn is not None):
            if current_config.get('DeadLetterConfig'):
                if (current_config['DeadLetterConfig']['TargetArn'] != dead_letter_arn):
                    func_kwargs.update({
                        'DeadLetterConfig': {
                            'TargetArn': dead_letter_arn,
                        },
                    })
            elif (dead_letter_arn != ''):
                func_kwargs.update({
                    'DeadLetterConfig': {
                        'TargetArn': dead_letter_arn,
                    },
                })
        if (current_config['Runtime'] != runtime):
            module.fail_json(msg='Cannot change runtime. Please recreate the function')
        if (vpc_subnet_ids or vpc_security_group_ids):
            if (len(vpc_subnet_ids) < 1):
                module.fail_json(msg='At least 1 subnet is required')
            if (len(vpc_security_group_ids) < 1):
                module.fail_json(msg='At least 1 security group is required')
            if ('VpcConfig' in current_config):
                current_vpc_subnet_ids = current_config['VpcConfig']['SubnetIds']
                current_vpc_security_group_ids = current_config['VpcConfig']['SecurityGroupIds']
                subnet_net_id_changed = (sorted(vpc_subnet_ids) != sorted(current_vpc_subnet_ids))
                vpc_security_group_ids_changed = (sorted(vpc_security_group_ids) != sorted(current_vpc_security_group_ids))
            if (('VpcConfig' not in current_config) or subnet_net_id_changed or vpc_security_group_ids_changed):
                func_kwargs.update({
                    'VpcConfig': {
                        'SubnetIds': vpc_subnet_ids,
                        'SecurityGroupIds': vpc_security_group_ids,
                    },
                })
        elif (('VpcConfig' in current_config) and ('VpcId' in current_config['VpcConfig']) and (current_config['VpcConfig']['VpcId'] != '')):
            func_kwargs.update({
                'VpcConfig': {
                    'SubnetIds': [],
                    'SecurityGroupIds': [],
                },
            })
        if (len(func_kwargs) > 1):
            try:
                if (not check_mode):
                    response = client.update_function_configuration(**func_kwargs)
                    current_version = response['Version']
                changed = True
            except (botocore.exceptions.ParamValidationError, botocore.exceptions.ClientError) as e:
                module.fail_json(msg=str(e))
        code_kwargs = {
            'FunctionName': name,
            'Publish': True,
        }
        if (s3_bucket and s3_key):
            code_kwargs.update({
                'S3Bucket': s3_bucket,
                'S3Key': s3_key,
            })
            if s3_object_version:
                code_kwargs.update({
                    'S3ObjectVersion': s3_object_version,
                })
        elif zip_file:
            local_checksum = sha256sum(zip_file)
            remote_checksum = current_config['CodeSha256']
            if (local_checksum != remote_checksum):
                try:
                    with open(zip_file, 'rb') as f:
                        encoded_zip = f.read()
                    code_kwargs.update({
                        'ZipFile': encoded_zip,
                    })
                except IOError as e:
                    module.fail_json(msg=str(e))
        if (len(code_kwargs) > 2):
            try:
                if (not check_mode):
                    response = client.update_function_code(**code_kwargs)
                    current_version = response['Version']
                changed = True
            except (botocore.exceptions.ParamValidationError, botocore.exceptions.ClientError) as e:
                module.fail_json(msg=str(e))
        response = get_current_function(client, name, qualifier=current_version)
        if (not response):
            module.fail_json(msg='Unable to get function information after updating')
        module.exit_json(changed=changed, **camel_dict_to_snake_dict(response))
    elif (state == 'present'):
        if (s3_bucket and s3_key):
            code = {
                'S3Bucket': s3_bucket,
                'S3Key': s3_key,
            }
            if s3_object_version:
                code.update({
                    'S3ObjectVersion': s3_object_version,
                })
        elif zip_file:
            try:
                with open(zip_file, 'rb') as f:
                    zip_content = f.read()
                code = {
                    'ZipFile': zip_content,
                }
            except IOError as e:
                module.fail_json(msg=str(e))
        else:
            module.fail_json(msg='Either S3 object or path to zipfile required')
        func_kwargs = {
            'FunctionName': name,
            'Description': description,
            'Publish': True,
            'Runtime': runtime,
            'Role': role_arn,
            'Handler': handler,
            'Code': code,
            'Timeout': timeout,
            'MemorySize': memory_size,
        }
        if environment_variables:
            func_kwargs.update({
                'Environment': {
                    'Variables': environment_variables,
                },
            })
        if dead_letter_arn:
            func_kwargs.update({
                'DeadLetterConfig': {
                    'TargetARN': dead_letter_arn,
                },
            })
        if (vpc_subnet_ids or vpc_security_group_ids):
            if (len(vpc_subnet_ids) < 1):
                module.fail_json(msg='At least 1 subnet is required')
            if (len(vpc_security_group_ids) < 1):
                module.fail_json(msg='At least 1 security group is required')
            func_kwargs.update({
                'VpcConfig': {
                    'SubnetIds': vpc_subnet_ids,
                    'SecurityGroupIds': vpc_security_group_ids,
                },
            })
        try:
            if (not check_mode):
                response = client.create_function(**func_kwargs)
                current_version = response['Version']
            changed = True
        except (botocore.exceptions.ParamValidationError, botocore.exceptions.ClientError) as e:
            module.fail_json(msg=str(e))
        response = get_current_function(client, name, qualifier=current_version)
        if (not response):
            module.fail_json(msg='Unable to get function information after creating')
        module.exit_json(changed=changed, **camel_dict_to_snake_dict(response))
    if ((state == 'absent') and current_function):
        try:
            if (not check_mode):
                client.delete_function(FunctionName=name)
            changed = True
        except (botocore.exceptions.ParamValidationError, botocore.exceptions.ClientError) as e:
            module.fail_json(msg=str(e))
        module.exit_json(changed=changed)
    elif (state == 'absent'):
        module.exit_json(changed=changed)
