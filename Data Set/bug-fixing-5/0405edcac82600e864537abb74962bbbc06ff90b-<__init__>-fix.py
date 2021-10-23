def __init__(self, module, region, **aws_connect_params):
    try:
        self.connection = boto3_conn(module, conn_type='client', resource='efs', region=region, **aws_connect_params)
        self.module = module
    except Exception as e:
        module.fail_json(msg=('Failed to connect to AWS: %s' % str(e)))
    self.region = region