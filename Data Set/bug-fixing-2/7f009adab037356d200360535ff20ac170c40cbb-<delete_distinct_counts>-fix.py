

def delete_distinct_counts(self, models, keys, start=None, end=None, timestamp=None, environment_ids=None):
    environment_ids = (set(environment_ids) if (environment_ids is not None) else set()).union([None])
    self.validate_arguments(models, environment_ids)
    rollups = self.get_active_series(start, end, timestamp)
    for (cluster, environment_ids) in self.get_cluster_groups(environment_ids):
        with cluster.fanout() as client:
            for (rollup, series) in rollups.items():
                for timestamp in series:
                    for model in models:
                        for key in keys:
                            c = client.target_key(key)
                            for environment_id in environment_ids:
                                c.delete(self.make_key(model, rollup, to_timestamp(timestamp), key, environment_id))
