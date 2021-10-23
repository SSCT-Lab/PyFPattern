

def raw_query(start, end, groupby=None, conditions=None, filter_keys=None, aggregations=None, rollup=None, arrayjoin=None, limit=None, offset=None, orderby=None, having=None, referrer=None, is_grouprelease=False, selected_columns=None, totals=None, limitby=None, turbo=False):
    '\n    Sends a query to snuba.\n\n    `conditions`: A list of (column, operator, literal) conditions to be passed\n    to the query. Conditions that we know will not have to be translated should\n    be passed this way (eg tag[foo] = bar).\n\n    `filter_keys`: A dictionary of {col: [key, ...]} that will be converted\n    into "col IN (key, ...)" conditions. These are used to restrict the query to\n    known sets of project/issue/environment/release etc. Appropriate\n    translations (eg. from environment model ID to environment name) are\n    performed on the query, and the inverse translation performed on the\n    result. The project_id(s) to restrict the query to will also be\n    automatically inferred from these keys.\n\n    `aggregations` a list of (aggregation_function, column, alias) tuples to be\n    passed to the query.\n    '
    start = naiveify_datetime(start)
    end = naiveify_datetime(end)
    groupby = (groupby or [])
    conditions = (conditions or [])
    having = (having or [])
    aggregations = (aggregations or [])
    filter_keys = (filter_keys or {
        
    })
    selected_columns = (selected_columns or [])
    with timer('get_snuba_map'):
        (forward, reverse) = get_snuba_translators(filter_keys, is_grouprelease=is_grouprelease)
    if ('project_id' in filter_keys):
        project_ids = list(set(filter_keys['project_id']))
    elif filter_keys:
        with timer('get_related_project_ids'):
            ids = [get_related_project_ids(k, filter_keys[k]) for k in filter_keys]
            project_ids = list(set.union(*map(set, ids)))
    else:
        project_ids = []
    for (col, keys) in six.iteritems(forward(filter_keys.copy())):
        if keys:
            if ((len(keys) == 1) and (None in keys)):
                conditions.append((col, 'IS NULL', None))
            else:
                conditions.append((col, 'IN', keys))
    if (not project_ids):
        raise UnqualifiedQueryError('No project_id filter, or none could be inferred from other filters.')
    project = Project.objects.get(pk=project_ids[0])
    retention = quotas.get_event_retention(organization=Organization(project.organization_id))
    if retention:
        start = max(start, (datetime.utcnow() - timedelta(days=retention)))
        if (start > end):
            raise QueryOutsideRetentionError
    (start, end) = shrink_time_window(filter_keys.get('issue'), start, end)
    if (start > end):
        raise QueryOutsideGroupActivityError
    request = {k: v for (k, v) in six.iteritems({
        'from_date': start.isoformat(),
        'to_date': end.isoformat(),
        'conditions': conditions,
        'having': having,
        'groupby': groupby,
        'totals': totals,
        'project': project_ids,
        'aggregations': aggregations,
        'granularity': rollup,
        'arrayjoin': arrayjoin,
        'limit': limit,
        'offset': offset,
        'limitby': limitby,
        'orderby': orderby,
        'selected_columns': selected_columns,
        'turbo': turbo,
    }) if (v is not None)}
    request.update(OVERRIDE_OPTIONS)
    headers = {
        
    }
    if referrer:
        headers['referer'] = referrer
    try:
        with timer('snuba_query'):
            response = _snuba_pool.urlopen('POST', '/query', body=json.dumps(request), headers=headers)
    except urllib3.exceptions.HTTPError as err:
        raise SnubaError(err)
    try:
        body = json.loads(response.data)
    except ValueError:
        raise UnexpectedResponseError('Could not decode JSON response: {}'.format(response.data))
    if (response.status != 200):
        if body.get('error'):
            error = body['error']
            if (response.status == 429):
                raise RateLimitExceeded(error['message'])
            elif (error['type'] == 'schema'):
                raise SchemaValidationError(error['message'])
            elif (error['type'] == 'clickhouse'):
                if (error['code'] == 43):
                    raise QueryIllegalTypeOfArgument(error['message'])
                elif (error['code'] == 241):
                    raise QueryMemoryLimitExceeded(error['message'])
                else:
                    raise QueryExecutionError(error['message'])
            else:
                raise SnubaError(error['message'])
        else:
            raise SnubaError('HTTP {}'.format(response.status))
    body['data'] = [reverse(d) for d in body['data']]
    return body
