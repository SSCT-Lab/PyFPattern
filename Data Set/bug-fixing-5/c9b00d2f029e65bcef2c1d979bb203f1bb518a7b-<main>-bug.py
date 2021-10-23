def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(iam_type=dict(default=None, required=True, choices=['user', 'group', 'role']), groups=dict(type='list', default=None, required=False), state=dict(default=None, required=True, choices=['present', 'absent', 'update']), password=dict(default=None, required=False, no_log=True), update_password=dict(default='always', required=False, choices=['always', 'on_create']), access_key_state=dict(default=None, required=False, choices=['active', 'inactive', 'create', 'remove', 'Active', 'Inactive', 'Create', 'Remove']), access_key_ids=dict(type='list', default=None, required=False), key_count=dict(type='int', default=1, required=False), name=dict(default=None, required=False), trust_policy_filepath=dict(default=None, required=False), trust_policy=dict(type='dict', default=None, required=False), new_name=dict(default=None, required=False), path=dict(default='/', required=False), new_path=dict(default=None, required=False)))
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=[['trust_policy', 'trust_policy_filepath']])
    if (not HAS_BOTO):
        module.fail_json(msg='This module requires boto, please install it')
    state = module.params.get('state').lower()
    iam_type = module.params.get('iam_type').lower()
    groups = module.params.get('groups')
    name = module.params.get('name')
    new_name = module.params.get('new_name')
    password = module.params.get('password')
    update_pw = module.params.get('update_password')
    path = module.params.get('path')
    new_path = module.params.get('new_path')
    key_count = module.params.get('key_count')
    key_state = module.params.get('access_key_state')
    trust_policy = module.params.get('trust_policy')
    trust_policy_filepath = module.params.get('trust_policy_filepath')
    key_ids = module.params.get('access_key_ids')
    if key_state:
        key_state = key_state.lower()
        if (any([(n in key_state) for n in ['active', 'inactive']]) and (not key_ids)):
            module.fail_json(changed=False, msg="At least one access key has to be defined in order to use 'active' or 'inactive'")
    if ((iam_type == 'user') and (module.params.get('password') is not None)):
        pwd = module.params.get('password')
    elif ((iam_type != 'user') and (module.params.get('password') is not None)):
        module.fail_json(msg='a password is being specified when the iam_type is not user. Check parameters')
    else:
        pwd = None
    if ((iam_type != 'user') and ((module.params.get('access_key_state') is not None) or (module.params.get('access_key_id') is not None))):
        module.fail_json(msg='the IAM type must be user, when IAM access keys are being modified. Check parameters')
    if ((iam_type == 'role') and (state == 'update')):
        module.fail_json(changed=False, msg='iam_type: role, cannot currently be updated, please specify present or absent')
    if trust_policy_filepath:
        try:
            with open(trust_policy_filepath, 'r') as json_data:
                trust_policy_doc = json.dumps(json.load(json_data))
        except Exception as e:
            module.fail_json(msg=((str(e) + ': ') + trust_policy_filepath))
    elif trust_policy:
        try:
            trust_policy_doc = json.dumps(trust_policy)
        except Exception as e:
            module.fail_json(msg=((str(e) + ': ') + trust_policy))
    else:
        trust_policy_doc = None
    (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module)
    try:
        if region:
            iam = connect_to_aws(boto.iam, region, **aws_connect_kwargs)
        else:
            iam = boto.iam.connection.IAMConnection(**aws_connect_kwargs)
    except boto.exception.NoAuthHandlerFound as e:
        module.fail_json(msg=str(e))
    result = {
        
    }
    changed = False
    try:
        orig_group_list = list_all_groups(iam)
        orig_user_list = list_all_users(iam)
        orig_role_list = list_all_roles(iam)
        orig_prof_list = list_all_instance_profiles(iam)
    except boto.exception.BotoServerError as err:
        module.fail_json(msg=err.message)
    if (iam_type == 'user'):
        been_updated = False
        user_groups = None
        user_exists = any([(n in [name, new_name]) for n in orig_user_list])
        if user_exists:
            current_path = iam.get_user(name).get_user_result.user['path']
            if ((not new_path) and (current_path != path)):
                new_path = path
                path = current_path
        if ((state == 'present') and (not user_exists) and (not new_name)):
            (meta, changed) = create_user(module, iam, name, password, path, key_state, key_count)
            keys = iam.get_all_access_keys(name).list_access_keys_result.access_key_metadata
            if groups:
                (user_groups, changed) = set_users_groups(module, iam, name, groups, been_updated, new_name)
            module.exit_json(user_meta=meta, groups=user_groups, keys=keys, changed=changed)
        elif ((state in ['present', 'update']) and user_exists):
            if (update_pw == 'on_create'):
                password = None
            if ((name not in orig_user_list) and (new_name in orig_user_list)):
                been_updated = True
            (name_change, key_list, user_changed) = update_user(module, iam, name, new_name, new_path, key_state, key_count, key_ids, password, been_updated)
            if (name_change and new_name):
                orig_name = name
                name = new_name
            if isinstance(groups, list):
                (user_groups, groups_changed) = set_users_groups(module, iam, name, groups, been_updated, new_name)
                if (groups_changed == user_changed):
                    changed = groups_changed
                else:
                    changed = True
            else:
                changed = user_changed
            if (new_name and new_path):
                module.exit_json(changed=changed, groups=user_groups, old_user_name=orig_name, new_user_name=new_name, old_path=path, new_path=new_path, keys=key_list)
            elif (new_name and (not new_path) and (not been_updated)):
                module.exit_json(changed=changed, groups=user_groups, old_user_name=orig_name, new_user_name=new_name, keys=key_list)
            elif (new_name and (not new_path) and been_updated):
                module.exit_json(changed=changed, groups=user_groups, user_name=new_name, keys=key_list, key_state=key_state)
            elif ((not new_name) and new_path):
                module.exit_json(changed=changed, groups=user_groups, user_name=name, old_path=path, new_path=new_path, keys=key_list)
            else:
                module.exit_json(changed=changed, groups=user_groups, user_name=name, keys=key_list)
        elif ((state == 'update') and (not user_exists)):
            module.fail_json(msg=('The user %s does not exist. No update made.' % name))
        elif (state == 'absent'):
            if user_exists:
                try:
                    set_users_groups(module, iam, name, '')
                    (del_meta, name, changed) = delete_user(module, iam, name)
                    module.exit_json(deleted_user=name, changed=changed)
                except Exception as ex:
                    module.fail_json(changed=changed, msg=str(ex))
            else:
                module.exit_json(changed=False, msg=('User %s is already absent from your AWS IAM users' % name))
    elif (iam_type == 'group'):
        group_exists = (name in orig_group_list)
        if ((state == 'present') and (not group_exists)):
            (new_group, changed) = create_group(module=module, iam=iam, name=name, path=path)
            module.exit_json(changed=changed, group_name=new_group)
        elif ((state in ['present', 'update']) and group_exists):
            (changed, updated_name, updated_path, cur_path) = update_group(module=module, iam=iam, name=name, new_name=new_name, new_path=new_path)
            if (new_path and new_name):
                module.exit_json(changed=changed, old_group_name=name, new_group_name=updated_name, old_path=cur_path, new_group_path=updated_path)
            if (new_path and (not new_name)):
                module.exit_json(changed=changed, group_name=name, old_path=cur_path, new_group_path=updated_path)
            if ((not new_path) and new_name):
                module.exit_json(changed=changed, old_group_name=name, new_group_name=updated_name, group_path=cur_path)
            if ((not new_path) and (not new_name)):
                module.exit_json(changed=changed, group_name=name, group_path=cur_path)
        elif ((state == 'update') and (not group_exists)):
            module.fail_json(changed=changed, msg=("Update Failed. Group %s doesn't seem to exist!" % name))
        elif (state == 'absent'):
            if (name in orig_group_list):
                (removed_group, changed) = delete_group(module=module, iam=iam, name=name)
                module.exit_json(changed=changed, delete_group=removed_group)
            else:
                module.exit_json(changed=changed, msg='Group already absent')
    elif (iam_type == 'role'):
        role_list = []
        if (state == 'present'):
            (changed, role_list, role_result, instance_profile_result) = create_role(module, iam, name, path, orig_role_list, orig_prof_list, trust_policy_doc)
        elif (state == 'absent'):
            (changed, role_list, role_result, instance_profile_result) = delete_role(module, iam, name, orig_role_list, orig_prof_list)
        elif (state == 'update'):
            module.fail_json(changed=False, msg='Role update not currently supported by boto.')
        module.exit_json(changed=changed, roles=role_list, role_result=role_result, instance_profile_result=instance_profile_result)