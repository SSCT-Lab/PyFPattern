def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(source_region=dict(required=True), source_image_id=dict(required=True), name=dict(), description=dict(default=''), encrypted=dict(type='bool', required=False), kms_key_id=dict(type='str', required=False), wait=dict(type='bool', default=False), wait_timeout=dict(default=1200), tags=dict(type='dict')))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    try:
        ec2 = ec2_connect(module)
    except boto.exception.NoAuthHandlerFound as e:
        module.fail_json(msg=str(e))
    try:
        (region, ec2_url, boto_params) = get_aws_connection_info(module)
    except boto.exception.NoAuthHandlerFound as e:
        module.fail_json(msg=str(e))
    if (not region):
        module.fail_json(msg='region must be specified')
    copy_image(module, ec2)