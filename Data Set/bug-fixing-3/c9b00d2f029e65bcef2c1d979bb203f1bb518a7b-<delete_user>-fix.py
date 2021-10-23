def delete_user(module, iam, name):
    changed = False
    try:
        current_keys = [ck['access_key_id'] for ck in iam.get_all_access_keys(name).list_access_keys_result.access_key_metadata]
        for key in current_keys:
            iam.delete_access_key(key, name)
        try:
            login_profile = iam.get_login_profiles(name).get_login_profile_response
        except boto.exception.BotoServerError as err:
            error_msg = boto_exception(err)
            if ('Cannot find Login Profile' in error_msg):
                iam.delete_user(name)
        else:
            iam.delete_login_profile(name)
            iam.delete_user(name)
    except Exception as ex:
        module.fail_json(changed=False, msg=('delete failed %s' % ex))
        if ('must detach all policies first' in error_msg):
            for policy in iam.get_all_user_policies(name).list_user_policies_result.policy_names:
                iam.delete_user_policy(name, policy)
            try:
                iam.delete_user(name)
            except boto.exception.BotoServerError as err:
                error_msg = boto_exception(err)
                if ('must detach all policies first' in error_msg):
                    module.fail_json(changed=changed, msg=('All inline polices have been removed. Though it appearsthat %s has Managed Polices. This is not currently supported by boto. Please detach the polices through the console and try again.' % name))
                else:
                    module.fail_json(changed=changed, msg=str(error_msg))
            else:
                changed = True
        else:
            module.fail_json(changed=changed, msg=str(error_msg))
    else:
        changed = True
    return (name, changed)