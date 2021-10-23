def role_action(module, iam, name, policy_name, skip, pdoc, state):
    policy_match = False
    changed = False
    try:
        current_policies = [cp for cp in iam.list_role_policies(name).list_role_policies_result.policy_names]
    except boto.exception.BotoServerError as e:
        if (e.error_code == 'NoSuchEntity'):
            module.exit_json(changed=False, msg='No such role, policy will be skipped.')
        else:
            module.fail_json(msg=e.message)
    try:
        matching_policies = []
        for pol in current_policies:
            if (urllib.unquote(iam.get_role_policy(name, pol).get_role_policy_result.policy_document) == pdoc):
                policy_match = True
                matching_policies.append(pol)
        if (state == 'present'):
            if ((not policy_match) or ((not skip) and (policy_name not in matching_policies))):
                changed = True
                iam.put_role_policy(name, policy_name, pdoc)
        elif (state == 'absent'):
            try:
                iam.delete_role_policy(name, policy_name)
                changed = True
            except boto.exception.BotoServerError as err:
                error_msg = boto_exception(err)
                if ('cannot be found.' in error_msg):
                    changed = False
                    module.exit_json(changed=changed, msg=('%s policy is already absent' % policy_name))
                else:
                    module.fail_json(msg=err.message)
        updated_policies = [cp for cp in iam.list_role_policies(name).list_role_policies_result.policy_names]
    except boto.exception.BotoServerError as err:
        error_msg = boto_exception(err)
        module.fail_json(changed=changed, msg=error_msg)
    return (changed, name, updated_policies)