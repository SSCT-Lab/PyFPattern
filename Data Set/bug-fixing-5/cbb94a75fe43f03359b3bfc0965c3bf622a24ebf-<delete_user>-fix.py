def delete_user(module, iam, name):
    changed = delete_dependencies_first(module, iam, name)
    try:
        iam.delete_user(name)
    except boto.exception.BotoServerError as ex:
        module.fail_json(changed=changed, msg=('Failed to delete user %s: %s' % (name, ex)), exception=traceback.format_exc())
    else:
        changed = True
    return (name, changed)