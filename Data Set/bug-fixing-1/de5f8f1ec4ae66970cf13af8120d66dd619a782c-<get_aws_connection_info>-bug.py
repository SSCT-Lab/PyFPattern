

def get_aws_connection_info(module, boto3=False):
    ec2_url = module.params.get('ec2_url')
    access_key = module.params.get('aws_access_key')
    secret_key = module.params.get('aws_secret_key')
    security_token = module.params.get('security_token')
    region = module.params.get('region')
    profile_name = module.params.get('profile')
    validate_certs = module.params.get('validate_certs')
    if (not ec2_url):
        if ('AWS_URL' in os.environ):
            ec2_url = os.environ['AWS_URL']
        elif ('EC2_URL' in os.environ):
            ec2_url = os.environ['EC2_URL']
    if (not access_key):
        if os.environ.get('AWS_ACCESS_KEY_ID'):
            access_key = os.environ['AWS_ACCESS_KEY_ID']
        elif os.environ.get('AWS_ACCESS_KEY'):
            access_key = os.environ['AWS_ACCESS_KEY']
        elif os.environ.get('EC2_ACCESS_KEY'):
            access_key = os.environ['EC2_ACCESS_KEY']
        elif boto.config.get('Credentials', 'aws_access_key_id'):
            access_key = boto.config.get('Credentials', 'aws_access_key_id')
        elif boto.config.get('default', 'aws_access_key_id'):
            access_key = boto.config.get('default', 'aws_access_key_id')
        else:
            access_key = None
    if (not secret_key):
        if os.environ.get('AWS_SECRET_ACCESS_KEY'):
            secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
        elif os.environ.get('AWS_SECRET_KEY'):
            secret_key = os.environ['AWS_SECRET_KEY']
        elif os.environ.get('EC2_SECRET_KEY'):
            secret_key = os.environ['EC2_SECRET_KEY']
        elif boto.config.get('Credentials', 'aws_secret_access_key'):
            secret_key = boto.config.get('Credentials', 'aws_secret_access_key')
        elif boto.config.get('default', 'aws_secret_access_key'):
            secret_key = boto.config.get('default', 'aws_secret_access_key')
        else:
            secret_key = None
    if (not region):
        if ('AWS_REGION' in os.environ):
            region = os.environ['AWS_REGION']
        elif ('AWS_DEFAULT_REGION' in os.environ):
            region = os.environ['AWS_DEFAULT_REGION']
        elif ('EC2_REGION' in os.environ):
            region = os.environ['EC2_REGION']
        elif (not boto3):
            region = boto.config.get('Boto', 'aws_region')
            if (not region):
                region = boto.config.get('Boto', 'ec2_region')
        elif HAS_BOTO3:
            region = botocore.session.get_session().get_config_variable('region')
        else:
            module.fail_json(msg='Boto3 is required for this module. Please install boto3 and try again')
    if (not security_token):
        if os.environ.get('AWS_SECURITY_TOKEN'):
            security_token = os.environ['AWS_SECURITY_TOKEN']
        elif os.environ.get('AWS_SESSION_TOKEN'):
            security_token = os.environ['AWS_SESSION_TOKEN']
        elif os.environ.get('EC2_SECURITY_TOKEN'):
            security_token = os.environ['EC2_SECURITY_TOKEN']
        elif boto.config.get('Credentials', 'aws_security_token'):
            security_token = boto.config.get('Credentials', 'aws_security_token')
        elif boto.config.get('default', 'aws_security_token'):
            security_token = boto.config.get('default', 'aws_security_token')
        else:
            security_token = None
    if (HAS_BOTO3 and boto3):
        boto_params = dict(aws_access_key_id=access_key, aws_secret_access_key=secret_key, aws_session_token=security_token)
        boto_params['verify'] = validate_certs
        if profile_name:
            boto_params['profile_name'] = profile_name
    else:
        boto_params = dict(aws_access_key_id=access_key, aws_secret_access_key=secret_key, security_token=security_token)
        if profile_name:
            boto_params['profile_name'] = profile_name
        boto_params['validate_certs'] = validate_certs
    for (param, value) in boto_params.items():
        if isinstance(value, binary_type):
            boto_params[param] = text_type(value, 'utf-8', 'strict')
    return (region, ec2_url, boto_params)
