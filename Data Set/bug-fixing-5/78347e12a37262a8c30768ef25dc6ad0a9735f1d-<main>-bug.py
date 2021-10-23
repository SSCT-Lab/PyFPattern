def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(name=dict(required=True), image_id=dict(), instance_id=dict(), key_name=dict(), security_groups=dict(default=[], type='list'), user_data=dict(), user_data_path=dict(type='path'), kernel_id=dict(), volumes=dict(type='list'), instance_type=dict(), state=dict(default='present', choices=['present', 'absent']), spot_price=dict(type='float'), ramdisk_id=dict(), instance_profile_name=dict(), ebs_optimized=dict(default=False, type='bool'), associate_public_ip_address=dict(type='bool'), instance_monitoring=dict(default=False, type='bool'), assign_public_ip=dict(type='bool'), classic_link_vpc_security_groups=dict(type='list'), classic_link_vpc_id=dict(), vpc_id=dict(), placement_tenancy=dict(default='default', choices=['default', 'dedicated'])))
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=[['user_data', 'user_data_path']])
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 required for this module')
    try:
        (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
        connection = boto3_conn(module, conn_type='client', resource='autoscaling', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except botocore.exceptions.NoRegionError:
        module.fail_json(msg='region must be specified as a parameter in AWS_DEFAULT_REGION environment variable or in boto configuration file')
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=('unable to establish connection - ' + str(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    state = module.params.get('state')
    if (state == 'present'):
        create_launch_config(connection, module)
    elif (state == 'absent'):
        delete_launch_config(connection, module)