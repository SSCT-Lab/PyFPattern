def main():
    argument_spec = ansible.module_utils.ec2.ec2_argument_spec()
    argument_spec.update(dict(policy_name=dict(required=True), policy_description=dict(required=False, default=''), policy=dict(type='json', required=False, default=None), make_default=dict(type='bool', required=False, default=True), only_version=dict(type='bool', required=False, default=False), fail_on_delete=dict(type='bool', required=False, default=True), state=dict(required=True, default=None, choices=['present', 'absent'])))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 is required for this module')
    name = module.params.get('policy_name')
    description = module.params.get('policy_description')
    state = module.params.get('state')
    default = module.params.get('make_default')
    only = module.params.get('only_version')
    policy = None
    if (module.params.get('policy') is not None):
        policy = json.dumps(json.loads(module.params.get('policy')))
    if ((state == 'present') and (policy is None)):
        module.fail_json(msg='if state is present policy is required')
    try:
        (region, ec2_url, aws_connect_kwargs) = ansible.module_utils.ec2.get_aws_connection_info(module, boto3=True)
        iam = ansible.module_utils.ec2.boto3_conn(module, conn_type='client', resource='iam', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except botocore.exceptions.NoCredentialsError as e:
        module.fail_json(msg=boto_exception(e))
    p = get_policy_by_name(iam, name)
    if (state == 'present'):
        if (p is None):
            rvalue = iam.create_policy(PolicyName=name, Path='/', PolicyDocument=policy, Description=description)
            module.exit_json(changed=True, policy=rvalue['Policy'])
        else:
            (policy_version, changed) = get_or_create_policy_version(iam, p, policy)
            changed = (set_if_default(iam, p, policy_version, default) or changed)
            changed = (set_if_only(iam, p, policy_version, only) or changed)
            if changed:
                p = iam.get_policy(PolicyArn=p['Arn'])['Policy']
            module.exit_json(changed=changed, policy=p)
    elif p:
        detach_all_entities(iam, p)
        for v in iam.list_policy_versions(PolicyArn=p['Arn'])['Versions']:
            if (not v['IsDefaultVersion']):
                iam.delete_policy_version(PolicyArn=p['Arn'], VersionId=v['VersionId'])
        iam.delete_policy(PolicyArn=p['Arn'])
        module.exit_json(changed=True, policy=p)
    else:
        module.exit_json(changed=False, policy=None)