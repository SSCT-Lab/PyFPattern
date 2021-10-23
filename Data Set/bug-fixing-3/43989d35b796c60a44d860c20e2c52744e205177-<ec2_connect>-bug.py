def ec2_connect(module):
    ' Return an ec2 connection'
    (region, ec2_url, boto_params) = get_aws_connection_info(module)
    if region:
        try:
            ec2 = connect_to_aws(boto.ec2, region, **boto_params)
        except (boto.exception.NoAuthHandlerFound, AnsibleAWSError) as e:
            module.fail_json(msg=str(e))
    elif ec2_url:
        try:
            ec2 = boto.connect_ec2_endpoint(ec2_url, **boto_params)
        except (boto.exception.NoAuthHandlerFound, AnsibleAWSError) as e:
            module.fail_json(msg=str(e))
    else:
        module.fail_json(msg='Either region or ec2_url must be specified')
    return ec2