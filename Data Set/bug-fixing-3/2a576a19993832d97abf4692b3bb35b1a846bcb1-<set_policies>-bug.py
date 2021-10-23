def set_policies(api, name, policies_list):
    updated = False
    try:
        if (policies_list is None):
            return False
        current_policies = get_policies(api, name)
        to_add_policies = []
        for x in policies_list:
            if (x not in current_policies):
                to_add_policies.append(x)
        to_del_policies = []
        for x in current_policies:
            if (x not in policies_list):
                to_del_policies.append(x)
        if (len(to_del_policies) > 0):
            api.LocalLB.VirtualServer.remove_content_policy(virtual_servers=[name], policies=[to_del_policies])
            updated = True
        if (len(to_add_policies) > 0):
            api.LocalLB.VirtualServer.add_content_policy(virtual_servers=[name], policies=[to_add_policies])
            updated = True
        return updated
    except bigsuds.OperationFailed as e:
        raise Exception(('Error on setting policies : %s' % e))