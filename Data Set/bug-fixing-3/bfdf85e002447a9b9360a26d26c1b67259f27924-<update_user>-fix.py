def update_user(module, iam, name, new_name, new_path, key_state, key_count, keys, pwd, updated):
    changed = False
    name_change = False
    if (updated and new_name):
        name = new_name
    try:
        current_keys = [ck['access_key_id'] for ck in iam.get_all_access_keys(name).list_access_keys_result.access_key_metadata]
        status = [ck['status'] for ck in iam.get_all_access_keys(name).list_access_keys_result.access_key_metadata]
        key_qty = len(current_keys)
    except boto.exception.BotoServerError as err:
        error_msg = boto_exception(err)
        if (('cannot be found' in error_msg) and updated):
            current_keys = [ck['access_key_id'] for ck in iam.get_all_access_keys(new_name).list_access_keys_result.access_key_metadata]
            status = [ck['status'] for ck in iam.get_all_access_keys(new_name).list_access_keys_result.access_key_metadata]
            name = new_name
        else:
            module.fail_json(changed=False, msg=str(err))
    updated_key_list = {
        
    }
    if (new_name or new_path):
        c_path = iam.get_user(name).get_user_result.user['path']
        if ((name != new_name) or (c_path != new_path)):
            changed = True
            try:
                if (not updated):
                    user = iam.update_user(name, new_user_name=new_name, new_path=new_path).update_user_response.response_metadata
                else:
                    user = iam.update_user(name, new_path=new_path).update_user_response.response_metadata
                user['updates'] = dict(old_username=name, new_username=new_name, old_path=c_path, new_path=new_path)
            except boto.exception.BotoServerError as err:
                error_msg = boto_exception(err)
                module.fail_json(changed=False, msg=str(err))
            else:
                if (not updated):
                    name_change = True
    if pwd:
        try:
            iam.update_login_profile(name, pwd)
            changed = True
        except boto.exception.BotoServerError:
            try:
                iam.create_login_profile(name, pwd)
                changed = True
            except boto.exception.BotoServerError as err:
                error_msg = boto_exception(str(err))
                if ('Password does not conform to the account password policy' in error_msg):
                    module.fail_json(changed=False, msg="Password doesn't conform to policy")
                else:
                    module.fail_json(msg=error_msg)
    try:
        current_keys = [ck['access_key_id'] for ck in iam.get_all_access_keys(name).list_access_keys_result.access_key_metadata]
        status = [ck['status'] for ck in iam.get_all_access_keys(name).list_access_keys_result.access_key_metadata]
        key_qty = len(current_keys)
    except boto.exception.BotoServerError as err:
        error_msg = boto_exception(err)
        if (('cannot be found' in error_msg) and updated):
            current_keys = [ck['access_key_id'] for ck in iam.get_all_access_keys(new_name).list_access_keys_result.access_key_metadata]
            status = [ck['status'] for ck in iam.get_all_access_keys(new_name).list_access_keys_result.access_key_metadata]
            name = new_name
        else:
            module.fail_json(changed=False, msg=str(err))
    new_keys = []
    if (key_state == 'create'):
        try:
            while (key_count > key_qty):
                new_keys.append(iam.create_access_key(user_name=name).create_access_key_response.create_access_key_result.access_key)
                key_qty += 1
                changed = True
        except boto.exception.BotoServerError as err:
            module.fail_json(changed=False, msg=str(err))
    if (keys and key_state):
        for access_key in keys:
            if (key_state in ('active', 'inactive')):
                if (access_key in current_keys):
                    for (current_key, current_key_state) in zip(current_keys, status):
                        if (key_state != current_key_state.lower()):
                            try:
                                iam.update_access_key(access_key, key_state.capitalize(), user_name=name)
                                changed = True
                            except boto.exception.BotoServerError as err:
                                module.fail_json(changed=False, msg=str(err))
                else:
                    module.fail_json(msg=('Supplied keys not found for %s. Current keys: %s. Supplied key(s): %s' % (name, current_keys, keys)))
            if (key_state == 'remove'):
                if (access_key in current_keys):
                    try:
                        iam.delete_access_key(access_key, user_name=name)
                    except boto.exception.BotoServerError as err:
                        module.fail_json(changed=False, msg=str(err))
                    else:
                        changed = True
    try:
        (final_keys, final_key_status) = ([ck['access_key_id'] for ck in iam.get_all_access_keys(name).list_access_keys_result.access_key_metadata], [ck['status'] for ck in iam.get_all_access_keys(name).list_access_keys_result.access_key_metadata])
    except boto.exception.BotoServerError as err:
        module.fail_json(changed=changed, msg=str(err))
    for (fk, fks) in zip(final_keys, final_key_status):
        updated_key_list.update({
            fk: fks,
        })
    return (name_change, updated_key_list, changed, new_keys)