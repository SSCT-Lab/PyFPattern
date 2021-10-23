def _get_quotas(cloud, project):
    quota = {
        
    }
    quota['volume'] = _get_volume_quotas(cloud, project)
    quota['network'] = _get_network_quotas(cloud, project)
    quota['compute'] = _get_compute_quotas(cloud, project)
    for quota_type in quota.keys():
        quota[quota_type] = _scrub_results(quota[quota_type])
    return quota