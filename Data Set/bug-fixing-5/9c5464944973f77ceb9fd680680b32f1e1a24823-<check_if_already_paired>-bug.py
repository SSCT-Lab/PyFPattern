def check_if_already_paired(self):
    '\n            Check for idempotency\n        '
    paired_clusters = self.elem.list_cluster_pairs()
    for pair in paired_clusters.cluster_pairs:
        if (pair.mvip == self.parameters['dest_mvip']):
            return pair.cluster_pair_id
    return None