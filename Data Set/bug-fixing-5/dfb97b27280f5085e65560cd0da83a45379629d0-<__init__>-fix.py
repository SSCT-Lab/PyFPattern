def __init__(self, module):
    self.module = module
    try:
        (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
        self.client = boto3_conn(module, conn_type='client', resource='cloudformation', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except botocore.exceptions.NoRegionError:
        self.module.fail_json(msg='Region must be specified as a parameter, in AWS_DEFAULT_REGION environment variable or in boto configuration file')
    except Exception as e:
        self.module.fail_json(msg=("Can't establish connection - " + str(e)), exception=traceback.format_exc())