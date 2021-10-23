def snuba_search(start, end, project_ids, environment_ids, sort_field, cursor=None, candidate_ids=None, limit=None, offset=0, get_sample=False, search_filters=None):
    "\n    This function doesn't strictly benefit from or require being pulled out of the main\n    query method above, but the query method is already large and this function at least\n    extracts most of the Snuba-specific logic.\n\n    Returns a tuple of:\n     * a sorted list of (group_id, group_score) tuples sorted descending by score,\n     * the count of total results (rows) available for this query.\n    "
    filters = {
        'project_id': project_ids,
    }
    if (environment_ids is not None):
        filters['environment'] = environment_ids
    if candidate_ids:
        filters['issue'] = candidate_ids
    conditions = []
    having = []
    for search_filter in search_filters:
        if ((search_filter.key.name in issue_only_fields) or (search_filter.key.name == 'date')):
            continue
        converted_filter = convert_search_filter_to_snuba_query(search_filter)
        if ((search_filter.key.name in aggregation_defs) and (not search_filter.key.is_tag)):
            having.append(converted_filter)
        else:
            conditions.append(converted_filter)
    extra_aggregations = dependency_aggregations.get(sort_field, [])
    required_aggregations = set(([sort_field, 'total'] + extra_aggregations))
    for h in having:
        alias = h[0]
        required_aggregations.add(alias)
    aggregations = []
    for alias in required_aggregations:
        aggregations.append((aggregation_defs[alias] + [alias]))
    if (cursor is not None):
        having.append((sort_field, ('>=' if cursor.is_prev else '<='), cursor.value))
    selected_columns = []
    if get_sample:
        query_hash = md5(repr(conditions)).hexdigest()[:8]
        selected_columns.append(('cityHash64', ("'{}'".format(query_hash), 'issue'), 'sample'))
        sort_field = 'sample'
        orderby = [sort_field]
        referrer = 'search_sample'
    else:
        orderby = ['-{}'.format(sort_field), 'issue']
        referrer = 'search'
    snuba_results = snuba.raw_query(start=start, end=end, selected_columns=selected_columns, groupby=['issue'], conditions=conditions, having=having, filter_keys=filters, aggregations=aggregations, orderby=orderby, referrer=referrer, limit=limit, offset=offset, totals=True, turbo=get_sample, sample=1)
    rows = snuba_results['data']
    total = snuba_results['totals']['total']
    if (not get_sample):
        metrics.timing('snuba.search.num_result_groups', len(rows))
    return ([(row['issue'], row[sort_field]) for row in rows], total)