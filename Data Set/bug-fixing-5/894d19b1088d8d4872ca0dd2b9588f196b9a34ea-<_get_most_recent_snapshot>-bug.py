def _get_most_recent_snapshot(snapshots, max_snapshot_age_secs=None, now=None):
    '\n    Gets the most recently created snapshot and optionally filters the result\n    if the snapshot is too old\n    :param snapshots: list of snapshots to search\n    :param max_snapshot_age_secs: filter the result if its older than this\n    :param now: simulate time -- used for unit testing\n    :return:\n    '
    if (len(snapshots) == 0):
        return None
    if (not now):
        now = datetime.datetime.utcnow()
    youngest_snapshot = max(snapshots, key=_get_snapshot_starttime)
    snapshot_start = datetime.datetime.strptime(youngest_snapshot.start_time, '%Y-%m-%dT%H:%M:%S.000Z')
    snapshot_age = (now - snapshot_start)
    if (max_snapshot_age_secs is not None):
        if (snapshot_age.total_seconds() > max_snapshot_age_secs):
            return None
    return youngest_snapshot