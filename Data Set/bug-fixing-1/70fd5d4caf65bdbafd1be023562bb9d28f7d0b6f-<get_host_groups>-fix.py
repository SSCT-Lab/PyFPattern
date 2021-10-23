

def get_host_groups(inventory, refresh=False, cloud=None):
    (cache_file, cache_expiration_time) = get_cache_settings(cloud)
    if is_cache_stale(cache_file, cache_expiration_time, refresh=refresh):
        groups = to_json(get_host_groups_from_cloud(inventory))
        with open(cache_file, 'w') as f:
            f.write(groups)
    else:
        with open(cache_file, 'r') as f:
            groups = f.read()
    return groups
