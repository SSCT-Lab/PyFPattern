def get_recommended_datastore(self, datastore_cluster_obj=None):
    '\n        Function to return Storage DRS recommended datastore from datastore cluster\n        Args:\n            datastore_cluster_obj: datastore cluster managed object\n\n        Returns: Name of recommended datastore from the given datastore cluster\n\n        '
    if (datastore_cluster_obj is None):
        return None
    sdrs_status = datastore_cluster_obj.podStorageDrsEntry.storageDrsConfig.podConfig.enabled
    if sdrs_status:
        pod_sel_spec = vim.storageDrs.PodSelectionSpec()
        pod_sel_spec.storagePod = datastore_cluster_obj
        storage_spec = vim.storageDrs.StoragePlacementSpec()
        storage_spec.podSelectionSpec = pod_sel_spec
        storage_spec.type = 'create'
        try:
            rec = self.content.storageResourceManager.RecommendDatastores(storageSpec=storage_spec)
            rec_action = rec.recommendations[0].action[0]
            return rec_action.destination.name
        except Exception:
            pass
    datastore = None
    datastore_freespace = 0
    for ds in datastore_cluster_obj.childEntity:
        if (isinstance(ds, vim.Datastore) and (ds.summary.freeSpace > datastore_freespace)):
            datastore = ds
            datastore_freespace = ds.summary.freeSpace
    if datastore:
        return datastore.name
    return None