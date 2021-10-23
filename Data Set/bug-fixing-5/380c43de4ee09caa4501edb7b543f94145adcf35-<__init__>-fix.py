def __init__(self, module):
    self.module = module
    try:
        (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
        self.client = boto3_conn(module, conn_type='client', resource='cloudformation', region=region, endpoint=ec2_url, **aws_connect_kwargs)
        backoff_wrapper = AWSRetry.jittered_backoff(retries=10, delay=3, max_delay=30)
        self.client.describe_stacks = backoff_wrapper(self.client.describe_stacks)
        self.client.list_stack_resources = backoff_wrapper(self.client.list_stack_resources)
        self.client.describe_stack_events = backoff_wrapper(self.client.describe_stack_events)
        self.client.get_stack_policy = backoff_wrapper(self.client.get_stack_policy)
        self.client.get_template = backoff_wrapper(self.client.get_template)
    except botocore.exceptions.NoRegionError:
        self.module.fail_json(msg='Region must be specified as a parameter, in AWS_DEFAULT_REGION environment variable or in boto configuration file')
    except Exception as e:
        self.module.fail_json(msg=("Can't establish connection - " + str(e)), exception=traceback.format_exc())