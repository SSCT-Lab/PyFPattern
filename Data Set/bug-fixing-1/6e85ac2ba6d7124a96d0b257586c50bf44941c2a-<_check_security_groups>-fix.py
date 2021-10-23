

def _check_security_groups(module, cloud, server):
    changed = False
    if (not (hasattr(cloud, 'add_server_security_groups') and hasattr(cloud, 'remove_server_security_groups'))):
        return (changed, server)
    module_security_groups = set(module.params['security_groups'])
    if (server.security_groups is not None):
        server_security_groups = set((sg.name for sg in server.security_groups))
    else:
        server_security_groups = set()
    add_sgs = (module_security_groups - server_security_groups)
    remove_sgs = (server_security_groups - module_security_groups)
    if add_sgs:
        cloud.add_server_security_groups(server, list(add_sgs))
        changed = True
    if remove_sgs:
        cloud.remove_server_security_groups(server, list(remove_sgs))
        changed = True
    return (changed, server)
