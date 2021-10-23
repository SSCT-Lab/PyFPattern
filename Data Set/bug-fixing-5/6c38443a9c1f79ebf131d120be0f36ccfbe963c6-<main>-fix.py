def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(names={
        'default': [],
        'type': 'list',
    }))
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True)
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    connection = boto3_conn(module, conn_type='client', resource='elb', region=region, endpoint=ec2_url, **aws_connect_params)
    try:
        elbs = list_elbs(connection, module.params.get('names'))
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, msg='Failed to get load balancer facts.')
    module.exit_json(elbs=elbs)