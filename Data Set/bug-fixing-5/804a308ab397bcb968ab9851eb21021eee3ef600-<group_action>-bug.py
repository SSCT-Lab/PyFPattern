def group_action(module, iam, name, policy_name, skip, pdoc, state):
    policy_match = False
    changed = False
    msg = ''
    try:
        current_policies = [cp for cp in iam.get_all_group_policies(name).list_group_policies_result.policy_names]
        matching_policies = []
        for pol in current_policies:
            if (urllib.unquote(iam.get_group_policy(name, pol).get_group_policy_result.policy_document) == pdoc):
                policy_match = True
                matching_policies.append(pol)
                msg = ('The policy document you specified already exists under the name %s.' % pol)
        if (state == 'present'):
            if ((not policy_match) or ((not skip) and (policy_name not in matching_policies))):
                changed = True
                iam.put_group_policy(name, policy_name, pdoc)
        elif (state == 'absent'):
            try:
                iam.delete_group_policy(name, policy_name)
                changed = True
            except boto.exception.BotoServerError as err:
                error_msg = boto_exception(err)
                if ('cannot be found.' in error_msg):
                    changed = False
                    module.exit_json(changed=changed, msg=('%s policy is already absent' % policy_name))
        updated_policies = [cp for cp in iam.get_all_group_policies(name).list_group_policies_result.policy_names]
    except boto.exception.BotoServerError as err:
        error_msg = boto_exception(err)
        module.fail_json(changed=changed, msg=error_msg)
    return (changed, name, updated_policies, msg)