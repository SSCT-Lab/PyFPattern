

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(instance_id=dict(), image_id=dict(), architecture=dict(default='x86_64'), kernel_id=dict(), virtualization_type=dict(default='hvm'), root_device_name=dict(), delete_snapshot=dict(default=False, type='bool'), name=dict(default=''), wait=dict(type='bool', default=False), wait_timeout=dict(default=900, type='int'), description=dict(default=''), no_reboot=dict(default=False, type='bool'), state=dict(default='present'), device_mapping=dict(type='list'), tags=dict(type='dict'), launch_permissions=dict(type='dict'), image_location=dict(), enhanced_networking=dict(type='bool'), billing_products=dict(type='list'), ramdisk_id=dict(), sriov_net_support=dict(), purge_tags=dict(type='bool', default=False)))
    module = AnsibleAWSModule(argument_spec=argument_spec, required_if=[['state', 'absent', ['image_id']]])
    try:
        (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
        connection = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except botocore.exceptions.NoRegionError:
        module.fail_json(msg='Region must be specified as a parameter in AWS_DEFAULT_REGION environment variable or in boto configuration file.')
    if (module.params.get('state') == 'absent'):
        deregister_image(module, connection)
    elif (module.params.get('state') == 'present'):
        if module.params.get('image_id'):
            update_image(module, connection, module.params.get('image_id'))
        if ((not module.params.get('instance_id')) and (not module.params.get('device_mapping'))):
            module.fail_json(msg='The parameters instance_id or device_mapping (register from EBS snapshot) are required for a new image.')
        create_image(module, connection)
