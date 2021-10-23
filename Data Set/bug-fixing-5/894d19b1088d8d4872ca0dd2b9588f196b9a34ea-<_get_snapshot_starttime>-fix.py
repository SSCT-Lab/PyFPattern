def _get_snapshot_starttime(snap):
    return datetime.datetime.strptime(snap.start_time, '%Y-%m-%dT%H:%M:%S.%fZ')