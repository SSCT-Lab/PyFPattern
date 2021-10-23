def _get_quotas(module, cloud, project):
    quota = {
        
    }
    try:
        quota['volume'] = _get_volume_quotas(cloud, project)
    except exceptions.EndpointNotFound:
        module.warn('No public endpoint for volumev2 service was found. Ignoring volume quotas.')
    try:
        quota['network'] = _get_network_quotas(cloud, project)
    except exceptions.EndpointNotFound:
        module.warn('No public endpoint for network service was found. Ignoring network quotas.')
    quota['compute'] = _get_compute_quotas(cloud, project)
    for quota_type in quota.keys():
        quota[quota_type] = _scrub_results(quota[quota_type])
    return quota