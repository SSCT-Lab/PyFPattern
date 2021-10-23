def _permissions_service(connection, module):
    if module.params['user_name']:
        service = connection.system_service().users_service()
        entity = next(iter(service.list(search='usrname={0}'.format('{0}@{1}'.format(module.params['user_name'], module.params['authz_name'])))), None)
    else:
        service = connection.system_service().groups_service()
        entity = search_by_name(service, module.params['group_name'])
    if (entity is None):
        raise Exception("User/Group wasn't found.")
    return service.service(entity.id).permissions_service()