def set_profiles(api, name, profiles_list):
    updated = False
    try:
        if (profiles_list is None):
            return False
        current_profiles = list(map((lambda x: x['profile_name']), get_profiles(api, name)))
        to_add_profiles = []
        for x in profiles_list:
            if (x not in current_profiles):
                to_add_profiles.append({
                    'profile_context': 'PROFILE_CONTEXT_TYPE_ALL',
                    'profile_name': x,
                })
        to_del_profiles = []
        for x in current_profiles:
            if ((x not in profiles_list) and (x != '/Common/tcp')):
                to_del_profiles.append({
                    'profile_context': 'PROFILE_CONTEXT_TYPE_ALL',
                    'profile_name': x,
                })
        if (len(to_del_profiles) > 0):
            api.LocalLB.VirtualServer.remove_profile(virtual_servers=[name], profiles=[to_del_profiles])
            updated = True
        if (len(to_add_profiles) > 0):
            api.LocalLB.VirtualServer.add_profile(virtual_servers=[name], profiles=[to_add_profiles])
            updated = True
        return updated
    except bigsuds.OperationFailed as e:
        raise Exception(('Error on setting profiles : %s' % e))