def delete_group(module=None, iam=None, name=None):
    changed = False
    try:
        iam.delete_group(name)
    except boto.exception.BotoServerError as err:
        error_msg = boto_exception(err)
        if ('must detach all policies first' in error_msg):
            for policy in iam.get_all_group_policies(name).list_group_policies_result.policy_names:
                iam.delete_group_policy(name, policy)
            try:
                iam.delete_group(name)
            except boto.exception.BotoServerError as err:
                error_msg = boto_exception(err)
                if ('must detach all policies first' in error_msg):
                    module.fail_json(changed=changed, msg=('All inline polices have been removed. Though it appearsthat %s has Managed Polices. This is not currently supported by boto. Please detach the polices through the console and try again.' % name))
                else:
                    module.fail_json(changed=changed, msg=str(err))
            else:
                changed = True
    else:
        changed = True
    return (changed, name)