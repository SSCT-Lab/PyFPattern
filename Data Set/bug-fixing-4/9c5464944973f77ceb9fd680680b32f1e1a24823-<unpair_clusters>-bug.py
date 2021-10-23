def unpair_clusters(self, pair_id):
    '\n            Delete cluster pair\n        '
    try:
        self.elem.remove_cluster_pair(cluster_pair_id=pair_id)
        self.dest_elem.remove_cluster_pair(cluster_pair_id=pair_id)
    except solidfire.common.ApiServerError as err:
        self.module.fail_json(msg=('Error unpairing cluster %s and %s' % (self.parameters['hostname'], self.parameters['dest_mvip'])), exception=to_native(err))