def get_cloudwatchevents_client(module):
    'Returns a boto3 client for accessing CloudWatch Events'
    try:
        (region, ec2_url, aws_conn_kwargs) = get_aws_connection_info(module, boto3=True)
        if (not region):
            module.fail_json(msg='Region must be specified as a parameter, in                              EC2_REGION or AWS_REGION environment variables                              or in boto configuration file')
        return boto3_conn(module, conn_type='client', resource='events', region=region, endpoint=ec2_url, **aws_conn_kwargs)
    except botocore.exceptions.ProfileNotFound as e:
        module.fail_json(msg=str(e))