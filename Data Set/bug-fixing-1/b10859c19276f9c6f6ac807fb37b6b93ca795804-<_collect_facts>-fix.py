

def _collect_facts(resource):
    'Transfrom cluster information to dict.'
    facts = {
        'identifier': resource['ClusterIdentifier'],
        'create_time': resource['ClusterCreateTime'],
        'status': resource['ClusterStatus'],
        'username': resource['MasterUsername'],
        'db_name': resource['DBName'],
        'availability_zone': resource['AvailabilityZone'],
        'maintenance_window': resource['PreferredMaintenanceWindow'],
        'url': resource['Endpoint']['Address'],
        'port': resource['Endpoint']['Port'],
    }
    for node in resource['ClusterNodes']:
        if (node['NodeRole'] in ('SHARED', 'LEADER')):
            facts['private_ip_address'] = node['PrivateIPAddress']
            facts['public_ip_address'] = node['PublicIPAddress']
            break
    return facts
