def query(start, end, groupby, conditions=None, filter_keys=None, aggregations=None, rollup=None, arrayjoin=None, limit=None, orderby=None, having=None, referrer=None, is_grouprelease=False, selected_columns=None):
    start = (start if (not start.tzinfo) else start.astimezone(pytz.utc).replace(tzinfo=None))
    end = (end if (not end.tzinfo) else end.astimezone(pytz.utc).replace(tzinfo=None))
    aggregations = (aggregations or [['count()', '', 'aggregate']])
    filter_keys = (filter_keys or {
        
    })
    selected_columns = (selected_columns or [])
    try:
        body = raw_query(start, end, groupby=groupby, conditions=conditions, filter_keys=filter_keys, selected_columns=selected_columns, aggregations=aggregations, rollup=rollup, arrayjoin=arrayjoin, limit=limit, orderby=orderby, having=having, referrer=referrer, is_grouprelease=is_grouprelease)
    except EntireQueryOutsideRetentionError:
        return OrderedDict()
    aggregate_cols = [a[2] for a in aggregations]
    expected_cols = set(((groupby + aggregate_cols) + selected_columns))
    got_cols = set((c['name'] for c in body['meta']))
    assert (expected_cols == got_cols)
    with timer('process_result'):
        return nest_groups(body['data'], groupby, aggregate_cols)