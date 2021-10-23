def ensure(module, client):
    state = module.params['state']
    name = module.params['cn']
    cmd = module.params['cmd']
    cmdcategory = module.params['cmdcategory']
    host = module.params['host']
    hostcategory = module.params['hostcategory']
    hostgroup = module.params['hostgroup']
    if (state in ['present', 'enabled']):
        ipaenabledflag = 'TRUE'
    else:
        ipaenabledflag = 'FALSE'
    sudoopt = module.params['sudoopt']
    user = module.params['user']
    usercategory = module.params['usercategory']
    usergroup = module.params['usergroup']
    module_sudorule = get_sudorule_dict(cmdcategory=cmdcategory, description=module.params['description'], hostcategory=hostcategory, ipaenabledflag=ipaenabledflag, usercategory=usercategory)
    ipa_sudorule = client.sudorule_find(name=name)
    changed = False
    if (state in ['present', 'disabled', 'enabled']):
        if (not ipa_sudorule):
            changed = True
            if (not module.check_mode):
                ipa_sudorule = client.sudorule_add(name=name, item=module_sudorule)
        else:
            diff = client.get_diff(ipa_sudorule, module_sudorule)
            if (len(diff) > 0):
                changed = True
                if (not module.check_mode):
                    if ('hostcategory' in diff):
                        if (ipa_sudorule.get('memberhost_host', None) is not None):
                            client.sudorule_remove_host_host(name=name, item=ipa_sudorule.get('memberhost_host'))
                        if (ipa_sudorule.get('memberhost_hostgroup', None) is not None):
                            client.sudorule_remove_host_hostgroup(name=name, item=ipa_sudorule.get('memberhost_hostgroup'))
                    client.sudorule_mod(name=name, item=module_sudorule)
        if (cmd is not None):
            changed = (category_changed(module, client, 'cmdcategory', ipa_sudorule) or changed)
            if (not module.check_mode):
                client.sudorule_add_allow_command(name=name, item=cmd)
        if (host is not None):
            changed = (category_changed(module, client, 'hostcategory', ipa_sudorule) or changed)
            changed = (client.modify_if_diff(name, ipa_sudorule.get('memberhost_host', []), host, client.sudorule_add_host_host, client.sudorule_remove_host_host) or changed)
        if (hostgroup is not None):
            changed = (category_changed(module, client, 'hostcategory', ipa_sudorule) or changed)
            changed = (client.modify_if_diff(name, ipa_sudorule.get('memberhost_hostgroup', []), hostgroup, client.sudorule_add_host_hostgroup, client.sudorule_remove_host_hostgroup) or changed)
        if (sudoopt is not None):
            ipa_list = ipa_sudorule.get('ipasudoopt', [])
            module_list = sudoopt
            diff = list((set(ipa_list) - set(module_list)))
            if (len(diff) > 0):
                changed = True
                if (not module.check_mode):
                    for item in diff:
                        client.sudorule_remove_option_ipasudoopt(name, item)
            diff = list((set(module_list) - set(ipa_list)))
            if (len(diff) > 0):
                changed = True
                if (not module.check_mode):
                    for item in diff:
                        client.sudorule_add_option_ipasudoopt(name, item)
        if (user is not None):
            changed = (category_changed(module, client, 'usercategory', ipa_sudorule) or changed)
            changed = (client.modify_if_diff(name, ipa_sudorule.get('memberuser_user', []), user, client.sudorule_add_user_user, client.sudorule_remove_user_user) or changed)
        if (usergroup is not None):
            changed = (category_changed(module, client, 'usercategory', ipa_sudorule) or changed)
            changed = (client.modify_if_diff(name, ipa_sudorule.get('memberuser_group', []), usergroup, client.sudorule_add_user_group, client.sudorule_remove_user_group) or changed)
    elif ipa_sudorule:
        changed = True
        if (not module.check_mode):
            client.sudorule_del(name)
    return (changed, client.sudorule_find(name))