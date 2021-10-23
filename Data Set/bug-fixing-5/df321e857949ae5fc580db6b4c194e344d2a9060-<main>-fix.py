def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(policy_name=dict(required=True), policy_description=dict(default=''), policy=dict(type='json'), make_default=dict(type='bool', default=True), only_version=dict(type='bool', default=False), fail_on_delete=dict(type='bool', default=True), state=dict(required=True, choices=['present', 'absent'])))
    module = AnsibleModule(argument_spec=argument_spec, required_if=[['state', 'present', ['policy']]])
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
    try:
        (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
        iam = boto3_conn(module, conn_type='client', resource='iam', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except (botocore.exceptions.NoCredentialsError, botocore.exceptions.ProfileNotFound) as e:
        module.fail_json(msg="Can't authorize connection. Check your credentials and profile.", exceptions=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    p = get_policy_by_name(module, iam, name)
    if (state == 'present'):
        if (p is None):
            try:
                rvalue = iam.create_policy(PolicyName=name, Path='/', PolicyDocument=policy, Description=description)
            except:
                module.fail_json(msg=("Couldn't create policy %s: %s" % (name, str(e))), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
            module.exit_json(changed=True, policy=camel_dict_to_snake_dict(rvalue['Policy']))
        else:
            (policy_version, changed) = get_or_create_policy_version(module, iam, p, policy)
            changed = (set_if_default(module, iam, p, policy_version, default) or changed)
            changed = (set_if_only(module, iam, p, policy_version, only) or changed)
            if changed:
                try:
                    p = iam.get_policy(PolicyArn=p['Arn'])['Policy']
                except:
                    module.fail_json(msg=("Couldn't get policy: %s" % str(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
            module.exit_json(changed=changed, policy=camel_dict_to_snake_dict(p))
    elif p:
        detach_all_entities(module, iam, p)
        try:
            versions = iam.list_policy_versions(PolicyArn=p['Arn'])['Versions']
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg=("Couldn't list policy versions: %s" % str(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        for v in versions:
            if (not v['IsDefaultVersion']):
                try:
                    iam.delete_policy_version(PolicyArn=p['Arn'], VersionId=v['VersionId'])
                except botocore.exceptions.ClientError as e:
                    module.fail_json(msg=("Couldn't delete policy version %s: %s" % (v['VersionId'], str(e))), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        try:
            iam.delete_policy(PolicyArn=p['Arn'])
        except:
            module.fail_json(msg=("Couldn't delete policy %s: %s" % (p['PolicyName'], str(e))), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        module.exit_json(changed=True, policy=camel_dict_to_snake_dict(p))
    else:
        module.exit_json(changed=False, policy=None)