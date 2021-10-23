

def get_data(self, model, keys, start, end, rollup=None, environment_ids=None, aggregation='count()', group_on_model=True, group_on_time=False):
    "\n        Normalizes all the TSDB parameters and sends a query to snuba.\n\n        `group_on_time`: whether to add a GROUP BY clause on the 'time' field.\n        `group_on_model`: whether to add a GROUP BY clause on the primary model.\n        "
    model_columns = self.model_columns.get(model)
    if (model_columns is None):
        raise Exception('Unsupported TSDBModel: {}'.format(model.name))
    (model_group, model_aggregate) = model_columns
    groupby = []
    if (group_on_model and (model_group is not None)):
        groupby.append(model_group)
    if group_on_time:
        groupby.append('time')
    if ((aggregation == 'count()') and (model_aggregate is not None)):
        groupby.append(model_aggregate)
        model_aggregate = None
    keys_map = dict(zip(model_columns, self.flatten_keys(keys)))
    keys_map = {k: v for (k, v) in six.iteritems(keys_map) if ((k is not None) and (v is not None))}
    if (environment_ids is not None):
        keys_map['environment'] = environment_ids
    aggregations = [[aggregation, model_aggregate, 'aggregate']]
    (rollup, series) = self.get_optimal_rollup_series(start, end, rollup)
    start = to_datetime(series[0])
    end = to_datetime((series[(- 1)] + rollup))
    limit = min(10000, int((len(keys) * ((end - start).total_seconds() / rollup))))
    if keys:
        result = snuba.query(start=start, end=end, groupby=groupby, conditions=None, filter_keys=keys_map, aggregations=aggregations, rollup=rollup, limit=limit, referrer='tsdb', is_grouprelease=(model == TSDBModel.frequent_releases_by_group))
    else:
        result = {
            
        }
    if group_on_time:
        keys_map['time'] = series
    self.zerofill(result, groupby, keys_map)
    self.trim(result, groupby, keys)
    return result
