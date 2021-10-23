

def delete_dependencies_first(module, iam, name):
    changed = False
    try:
        current_keys = [ck['access_key_id'] for ck in iam.get_all_access_keys(name).list_access_keys_result.access_key_metadata]
        for key in current_keys:
            iam.delete_access_key(key, name)
        changed = True
    except boto.exception.BotoServerError as err:
        module.fail_json(changed=changed, msg=('Failed to delete keys: %s' % err), exception=traceback.format_exc())
    try:
        login_profile = iam.get_login_profiles(name).get_login_profile_response
        iam.delete_login_profile(name)
        changed = True
    except boto.exception.BotoServerError as err:
        error_msg = boto_exception(err)
        if ((('Login Profile for User ' + name) + ' cannot be found.') not in error_msg):
            module.fail_json(changed=changed, msg=('Failed to delete login profile: %s' % err), exception=traceback.format_exc())
    try:
        for policy in iam.get_all_user_policies(name).list_user_policies_result.policy_names:
            iam.delete_user_policy(name, policy)
        changed = True
    except boto.exception.BotoServerError as err:
        error_msg = boto_exception(err)
        if ('must detach all policies first' in error_msg):
            module.fail_json(changed=changed, msg=('All inline polices have been removed. Though it appearsthat %s has Managed Polices. This is not currently supported by boto. Please detach the polices through the console and try again.' % name))
        module.fail_json(changed=changed, msg=('Failed to delete policies: %s' % err), exception=traceback.format_exc())
    try:
        mfa_devices = iam.get_all_mfa_devices(name).get('list_mfa_devices_response', {
            
        }).get('list_mfa_devices_result', {
            
        }).get('mfa_devices', [])
        for device in mfa_devices:
            iam.deactivate_mfa_device(name, device['serial_number'])
        changed = True
    except boto.exception.BotoServerError as err:
        module.fail_json(changed=changed, msg=('Failed to deactivate associated MFA devices: %s' % err), exception=traceback.format_exc())
    return changed
