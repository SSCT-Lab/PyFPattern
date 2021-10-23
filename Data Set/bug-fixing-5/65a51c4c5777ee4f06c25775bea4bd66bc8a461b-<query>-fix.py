def query(start, end, groupby, conditions=None, filter_keys=None, aggregations=None, rollup=None, arrayjoin=None, limit=None, orderby=None):
    '\n    Sends a query to snuba.\n\n    `conditions`: A list of (column, operator, literal) conditions to be passed\n    to the query. Conditions that we know will not have to be translated should\n    be passed this way (eg tag[foo] = bar).\n\n    `filter_keys`: A dictionary of {col: [key, ...]} that will be converted\n    into "col IN (key, ...)" conditions. These are used to restrict the query to\n    known sets of project/issue/environment/release etc. Appropriate\n    translations (eg. from environment model ID to environment name) are\n    performed on the query, and the inverse translation performed on the\n    result. The project_id(s) to restrict the query to will also be\n    automatically inferred from these keys.\n\n    `aggregations` a list of (aggregation_function, column, alias) tuples to be\n    passed to the query.\n    '
    groupby = (groupby or [])
    conditions = (conditions or [])
    aggregations = (aggregations or [['count()', '', 'aggregate']])
    filter_keys = (filter_keys or {
        
    })
    snuba_map = {col: get_snuba_map(col, keys) for (col, keys) in six.iteritems(filter_keys)}
    snuba_map = {k: v for (k, v) in six.iteritems(snuba_map) if ((k is not None) and (v is not None))}
    rev_snuba_map = {col: dict((reversed(i) for i in keys.items())) for (col, keys) in six.iteritems(snuba_map)}
    for (col, keys) in six.iteritems(filter_keys):
        keys = [k for k in keys if (k is not None)]
        if (col in snuba_map):
            keys = [snuba_map[col][k] for k in keys if (k in snuba_map[col])]
        if keys:
            conditions.append((col, 'IN', keys))
    if ('project_id' in filter_keys):
        project_ids = filter_keys['project_id']
    elif filter_keys:
        ids = [get_related_project_ids(k, filter_keys[k]) for k in filter_keys]
        project_ids = list(set.union(*map(set, ids)))
    else:
        project_ids = []
    if (not project_ids):
        raise SnubaError('No project_id filter, or none could be inferred from other filters.')
    aggregate_cols = [a[1] for a in aggregations]
    condition_cols = [c[0] for c in flat_conditions(conditions)]
    all_cols = ((groupby + aggregate_cols) + condition_cols)
    get_issues = ('issue' in all_cols)
    issues = (get_project_issues(project_ids, filter_keys.get('issue')) if get_issues else None)
    url = '{0}/query'.format(SNUBA)
    request = {k: v for (k, v) in six.iteritems({
        'from_date': start.isoformat(),
        'to_date': end.isoformat(),
        'conditions': conditions,
        'groupby': groupby,
        'project': project_ids,
        'aggregations': aggregations,
        'granularity': rollup,
        'issues': issues,
        'arrayjoin': arrayjoin,
        'limit': limit,
        'orderby': orderby,
    }) if (v is not None)}
    try:
        response = requests.post(url, data=json.dumps(request))
        response.raise_for_status()
    except requests.RequestException as re:
        raise SnubaError(re)
    try:
        response = json.loads(response.text)
    except ValueError:
        raise SnubaError('Could not decode JSON response: {}'.format(response.text))
    aggregate_cols = [a[2] for a in aggregations]
    expected_cols = set((groupby + aggregate_cols))
    got_cols = set((c['name'] for c in response['meta']))
    assert (expected_cols == got_cols)
    for d in response['data']:
        if ('time' in d):
            d['time'] = int(to_timestamp(parse_datetime(d['time'])))
        for col in rev_snuba_map:
            if (col in d):
                d[col] = rev_snuba_map[col][d[col]]
    return nest_groups(response['data'], groupby, aggregate_cols)