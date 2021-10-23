def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(default='present', choices=['present', 'absent']), region=dict(required=True), name=dict(), vpn_gateway_id=dict(), vpc_id=dict(), wait_timeout=dict(type='int', default=320), type=dict(default='ipsec.1', choices=['ipsec.1']), tags=dict(default=None, required=False, type='dict', aliases=['resource_tags'])))
    module = AnsibleModule(argument_spec=argument_spec, required_if=[['state', 'present', ['name']]])
    if (not HAS_BOTO3):
        module.fail_json(msg='json and boto3 is required.')
    state = module.params.get('state').lower()
    try:
        (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
        client = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except botocore.exceptions.NoCredentialsError as e:
        module.fail_json(msg=("Can't authorize connection - %s" % to_native(e)), exception=traceback.format_exc())
    if (state == 'present'):
        (changed, results) = ensure_vgw_present(client, module)
    else:
        (changed, results) = ensure_vgw_absent(client, module)
    module.exit_json(changed=changed, vgw=results)