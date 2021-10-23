def list_snapshots_recursively(self, snapshots):
    snapshot_data = []
    for snapshot in snapshots:
        snap_text = ('Id: %s; Name: %s; Description: %s; CreateTime: %s; State: %s' % (snapshot.id, snapshot.name, snapshot.description, snapshot.createTime, snapshot.state))
        snapshot_data.append(snap_text)
        snapshot_data = (snapshot_data + self.list_snapshots_recursively(snapshot.childSnapshotList))
    return snapshot_data