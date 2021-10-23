

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(command=dict(choices=['create', 'facts', 'delete', 'modify'], required=True), identifier=dict(required=True), node_type=dict(choices=['ds1.xlarge', 'ds1.8xlarge', 'ds2.xlarge', 'ds2.8xlarge', 'dc1.large', 'dc1.8xlarge', 'dw1.xlarge', 'dw1.8xlarge', 'dw2.large', 'dw2.8xlarge'], required=False), username=dict(required=False), password=dict(no_log=True, required=False), db_name=dict(require=False), cluster_type=dict(choices=['multi-node', 'single-node'], default='single-node'), cluster_security_groups=dict(aliases=['security_groups'], type='list'), vpc_security_group_ids=dict(aliases=['vpc_security_groups'], type='list'), cluster_subnet_group_name=dict(aliases=['subnet']), availability_zone=dict(aliases=['aws_zone', 'zone']), preferred_maintenance_window=dict(aliases=['maintance_window', 'maint_window']), cluster_parameter_group_name=dict(aliases=['param_group_name']), automated_snapshot_retention_period=dict(aliases=['retention_period']), port=dict(type='int'), cluster_version=dict(aliases=['version'], choices=['1.0']), allow_version_upgrade=dict(aliases=['version_upgrade'], type='bool', default=True), number_of_nodes=dict(type='int'), publicly_accessible=dict(type='bool', default=False), encrypted=dict(type='bool', default=False), elastic_ip=dict(required=False), new_cluster_identifier=dict(aliases=['new_identifier']), wait=dict(type='bool', default=False), wait_timeout=dict(default=300)))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO):
        module.fail_json(msg='boto v2.9.0+ required for this module')
    command = module.params.get('command')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module)
    if (not region):
        module.fail_json(msg=str('region not specified and unable to determine region from EC2_REGION.'))
    try:
        conn = connect_to_aws(boto.redshift, region, **aws_connect_params)
    except boto.exception.JSONResponseError as e:
        module.fail_json(msg=str(e))
    changed = True
    if (command == 'create'):
        (changed, cluster) = create_cluster(module, conn)
    elif (command == 'facts'):
        (changed, cluster) = describe_cluster(module, conn)
    elif (command == 'delete'):
        (changed, cluster) = delete_cluster(module, conn)
    elif (command == 'modify'):
        (changed, cluster) = modify_cluster(module, conn)
    module.exit_json(changed=changed, cluster=cluster)
