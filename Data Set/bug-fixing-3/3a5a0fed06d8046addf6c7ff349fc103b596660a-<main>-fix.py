def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(source_region=dict(required=True), source_image_id=dict(required=True), name=dict(default='default'), description=dict(default=''), encrypted=dict(type='bool', default=False, required=False), kms_key_id=dict(type='str', required=False), wait=dict(type='bool', default=False), wait_timeout=dict(type='int', default=600), tags=dict(type='dict')))
    module = AnsibleModule(argument_spec=argument_spec)
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    ec2 = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_params)
    copy_image(module, ec2)