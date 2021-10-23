

def create_role(module, iam, name, path, role_list, prof_list, trust_policy_doc):
    changed = False
    iam_role_result = None
    instance_profile_result = None
    try:
        if (name not in role_list):
            changed = True
            iam_role_result = iam.create_role(name, assume_role_policy_document=trust_policy_doc, path=path).create_role_response.create_role_result.role.role_name
            if (name not in prof_list):
                instance_profile_result = iam.create_instance_profile(name, path=path).create_instance_profile_response.create_instance_profile_result.instance_profile
                iam.add_role_to_instance_profile(name, name)
    except boto.exception.BotoServerError as err:
        module.fail_json(changed=changed, msg=str(err))
    else:
        updated_role_list = list_all_roles(iam)
    return (changed, updated_role_list, iam_role_result, instance_profile_result)
