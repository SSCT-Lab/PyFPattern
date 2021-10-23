def vs_create(api, name, destination, port, pool, profiles):
    if profiles:
        _profiles = []
        for profile in profiles:
            _profiles.append(dict(profile_context='PROFILE_CONTEXT_TYPE_ALL', profile_name=profile))
    else:
        _profiles = [{
            'profile_context': 'PROFILE_CONTEXT_TYPE_ALL',
            'profile_name': 'tcp',
        }]
    try:
        api.LocalLB.VirtualServer.create(definitions=[{
            'name': [name],
            'address': [destination],
            'port': port,
            'protocol': 'PROTOCOL_TCP',
        }], wildmasks=['255.255.255.255'], resources=[{
            'type': 'RESOURCE_TYPE_POOL',
            'default_pool_name': pool,
        }], profiles=[_profiles])
        created = True
        return created
    except bigsuds.OperationFailed as e:
        raise Exception(('Error on creating Virtual Server : %s' % e))