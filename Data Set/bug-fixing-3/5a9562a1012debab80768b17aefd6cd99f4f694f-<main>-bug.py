def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(image_ids=dict(default=[], type='list', aliases=['image_id']), filters=dict(default={
        
    }, type='dict'), owners=dict(default=[], type='list', aliases=['owner']), executable_users=dict(default=[], type='list', aliases=['executable_user'])))
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True)
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    if region:
        ec2_client = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_params)
    else:
        module.fail_json(msg='region must be specified')
    list_ec2_images(ec2_client, module)