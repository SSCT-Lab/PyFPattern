def is_group_env_installed(name, conf_file, installroot='/'):
    name_lower = name.lower()
    my = yum_base(conf_file, installroot)
    if (yum.__version_info__ >= (3, 4)):
        groups_list = my.doGroupLists(return_evgrps=True)
    else:
        groups_list = my.doGroupLists()
    groups = groups_list[0]
    for group in groups:
        if (name_lower.endswith(group.name.lower()) or name_lower.endswith(group.groupid.lower())):
            return True
    if (yum.__version_info__ >= (3, 4)):
        envs = groups_list[2]
        for env in envs:
            if (name_lower.endswith(env.name.lower()) or name_lower.endswith(env.environmentid.lower())):
                return True
    return False