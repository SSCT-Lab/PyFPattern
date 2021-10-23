

def get_range(self, model, keys, start, end, rollup=None, environment_ids=None):
    '\n        To get a range of data for group ID=[1, 2, 3]:\n\n        >>> now = timezone.now()\n        >>> get_keys(TimeSeriesModel.group, [1, 2, 3],\n        >>>          start=now - timedelta(days=1),\n        >>>          end=now)\n        '
    if ((environment_ids is not None) and (len(environment_ids) > 1)):
        raise NotImplementedError
    environment_id = (environment_ids[0] if environment_ids else None)
    self.validate_arguments([model], [environment_id])
    (rollup, series) = self.get_optimal_rollup_series(start, end, rollup)
    series = map(to_datetime, series)
    results = []
    (cluster, _) = self.get_cluster(environment_id)
    with cluster.map() as client:
        for key in keys:
            for timestamp in series:
                (hash_key, hash_field) = self.make_counter_key(model, rollup, timestamp, key, environment_id)
                results.append((to_timestamp(timestamp), key, client.hget(hash_key, hash_field)))
    results_by_key = defaultdict(dict)
    for (epoch, key, count) in results:
        results_by_key[key][epoch] = int((count.value or 0))
    for (key, points) in six.iteritems(results_by_key):
        results_by_key[key] = sorted(points.items())
    return dict(results_by_key)
