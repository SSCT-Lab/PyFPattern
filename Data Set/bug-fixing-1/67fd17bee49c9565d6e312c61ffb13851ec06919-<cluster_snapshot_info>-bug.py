

def cluster_snapshot_info(module, conn):
    snapshot_name = module.params.get('db_cluster_snapshot_identifier')
    snapshot_type = module.params.get('snapshot_type')
    instance_name = module.params.get('db_cluster_instance_identifier')
    params = dict()
    if snapshot_name:
        params['DBClusterSnapshotIdentifier'] = snapshot_name
    if instance_name:
        params['DBClusterInstanceIdentifier'] = instance_name
    if snapshot_type:
        params['SnapshotType'] = snapshot_type
        if (snapshot_type == 'public'):
            params['IsPublic'] = True
        elif (snapshot_type == 'shared'):
            params['IsShared'] = True
    return common_snapshot_info(module, conn, 'describe_db_cluster_snapshots', 'DBClusterSnapshot', params)
