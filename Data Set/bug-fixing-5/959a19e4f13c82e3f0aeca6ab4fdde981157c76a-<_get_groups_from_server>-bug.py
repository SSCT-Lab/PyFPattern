def _get_groups_from_server(self, server_vars, namegroup=True):
    groups = []
    region = server_vars['region']
    cloud = server_vars['cloud']
    metadata = server_vars.get('metadata', {
        
    })
    groups.append(cloud)
    groups.append(region)
    groups.append(('%s_%s' % (cloud, region)))
    if ('group' in metadata):
        groups.append(metadata['group'])
    for extra_group in metadata.get('groups', '').split(','):
        if extra_group:
            groups.append(extra_group.strip())
    groups.append(('instance-%s' % server_vars['id']))
    if namegroup:
        groups.append(server_vars['name'])
    for key in ('flavor', 'image'):
        if ('name' in server_vars[key]):
            groups.append(('%s-%s' % (key, server_vars[key]['name'])))
    for (key, value) in iter(metadata.items()):
        groups.append(('meta-%s_%s' % (key, value)))
    az = server_vars.get('az', None)
    if az:
        groups.append(az)
        groups.append(('%s_%s' % (region, az)))
        groups.append(('%s_%s_%s' % (cloud, region, az)))
    return groups