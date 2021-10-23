

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent']), group_name=dict(required=True, aliases=['name']), group_description=dict(required=False, aliases=['description']), group_subnets=dict(required=False, aliases=['subnets'], type='list')))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO):
        module.fail_json(msg='boto v2.9.0+ required for this module')
    state = module.params.get('state')
    group_name = module.params.get('group_name')
    group_description = module.params.get('group_description')
    group_subnets = module.params.get('group_subnets')
    if (state == 'present'):
        for required in ('group_name', 'group_description', 'group_subnets'):
            if (not module.params.get(required)):
                module.fail_json(msg=str(("parameter %s required for state='present'" % required)))
    else:
        for not_allowed in ('group_description', 'group_subnets'):
            if module.params.get(not_allowed):
                module.fail_json(msg=str(("parameter %s not allowed for state='absent'" % not_allowed)))
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module)
    if (not region):
        module.fail_json(msg=str('Region must be specified as a parameter, in EC2_REGION or AWS_REGION environment variables or in boto configuration file'))
    try:
        conn = connect_to_aws(boto.redshift, region, **aws_connect_params)
    except boto.exception.JSONResponseError as e:
        module.fail_json(msg=str(e))
    try:
        changed = False
        exists = False
        group = None
        try:
            matching_groups = conn.describe_cluster_subnet_groups(group_name, max_records=100)
            exists = (len(matching_groups) > 0)
        except boto.exception.JSONResponseError as e:
            if (e.body['Error']['Code'] != 'ClusterSubnetGroupNotFoundFault'):
                module.fail_json(msg=str(e))
        if (state == 'absent'):
            if exists:
                conn.delete_cluster_subnet_group(group_name)
                changed = True
        else:
            if (not exists):
                new_group = conn.create_cluster_subnet_group(group_name, group_description, group_subnets)
                group = {
                    'name': new_group['CreateClusterSubnetGroupResponse']['CreateClusterSubnetGroupResult']['ClusterSubnetGroup']['ClusterSubnetGroupName'],
                    'vpc_id': new_group['CreateClusterSubnetGroupResponse']['CreateClusterSubnetGroupResult']['ClusterSubnetGroup']['VpcId'],
                }
            else:
                changed_group = conn.modify_cluster_subnet_group(group_name, group_subnets, description=group_description)
                group = {
                    'name': changed_group['ModifyClusterSubnetGroupResponse']['ModifyClusterSubnetGroupResult']['ClusterSubnetGroup']['ClusterSubnetGroupName'],
                    'vpc_id': changed_group['ModifyClusterSubnetGroupResponse']['ModifyClusterSubnetGroupResult']['ClusterSubnetGroup']['VpcId'],
                }
            changed = True
    except boto.exception.JSONResponseError as e:
        module.fail_json(msg=str(e))
    module.exit_json(changed=changed, group=group)
