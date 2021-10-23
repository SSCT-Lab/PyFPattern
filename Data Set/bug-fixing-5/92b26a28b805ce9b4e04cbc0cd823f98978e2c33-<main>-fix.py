def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(source_region=dict(required=True), source_image_id=dict(required=True), name=dict(default='default'), description=dict(default=''), encrypted=dict(type='bool', required=False), kms_key_id=dict(type='str', required=False), wait=dict(type='bool', default=False), wait_timeout=dict(default=1200), tags=dict(type='dict')))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    if HAS_BOTO3:
        try:
            ec2 = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_params)
        except NoRegionError:
            module.fail_json(msg='AWS Region is required')
    else:
        module.fail_json(msg='boto3 required for this module')
    copy_image(module, ec2)