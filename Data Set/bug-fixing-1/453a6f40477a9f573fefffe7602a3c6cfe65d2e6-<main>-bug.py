

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(iam_type=dict(default=None, required=True, choices=['user', 'group', 'role']), state=dict(default=None, required=True, choices=['present', 'absent']), iam_name=dict(default=None, required=False), policy_name=dict(default=None, required=True), policy_document=dict(default=None, required=False), policy_json=dict(type='json', default=None, required=False), skip_duplicates=dict(type='bool', default=True, required=False)))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    state = module.params.get('state').lower()
    iam_type = module.params.get('iam_type').lower()
    state = module.params.get('state')
    name = module.params.get('iam_name')
    policy_name = module.params.get('policy_name')
    skip = module.params.get('skip_duplicates')
    if ((module.params.get('policy_document') is not None) and (module.params.get('policy_json') is not None)):
        module.fail_json(msg='Only one of "policy_document" or "policy_json" may be set')
    if (module.params.get('policy_document') is not None):
        with open(module.params.get('policy_document'), 'r') as json_data:
            pdoc = json.dumps(json.load(json_data))
            json_data.close()
    elif (module.params.get('policy_json') is not None):
        pdoc = module.params.get('policy_json')
        if (not isinstance(pdoc, string_types)):
            try:
                pdoc = json.dumps(pdoc)
            except Exception as e:
                module.fail_json(msg=('Failed to convert the policy into valid JSON: %s' % str(e)))
    else:
        pdoc = None
    (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module)
    try:
        if region:
            iam = connect_to_aws(boto.iam, region, **aws_connect_kwargs)
        else:
            iam = boto.iam.connection.IAMConnection(**aws_connect_kwargs)
    except boto.exception.NoAuthHandlerFound as e:
        module.fail_json(msg=str(e))
    changed = False
    if (iam_type == 'user'):
        (changed, user_name, current_policies) = user_action(module, iam, name, policy_name, skip, pdoc, state)
        module.exit_json(changed=changed, user_name=name, policies=current_policies)
    elif (iam_type == 'role'):
        (changed, role_name, current_policies) = role_action(module, iam, name, policy_name, skip, pdoc, state)
        module.exit_json(changed=changed, role_name=name, policies=current_policies)
    elif (iam_type == 'group'):
        (changed, group_name, current_policies, msg) = group_action(module, iam, name, policy_name, skip, pdoc, state)
        module.exit_json(changed=changed, group_name=name, policies=current_policies, msg=msg)
