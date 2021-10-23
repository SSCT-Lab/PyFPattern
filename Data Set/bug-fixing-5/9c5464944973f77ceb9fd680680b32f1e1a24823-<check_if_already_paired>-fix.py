def check_if_already_paired(self, paired_clusters, hostname):
    for pair in paired_clusters.cluster_pairs:
        if (pair.mvip == hostname):
            return pair.cluster_pair_id
    return None