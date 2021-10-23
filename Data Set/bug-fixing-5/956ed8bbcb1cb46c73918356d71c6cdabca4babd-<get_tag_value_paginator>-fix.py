def get_tag_value_paginator(self, project_id, environment_id, key, query=None, order_by='-last_seen'):
    from sentry.api.paginator import SequencePaginator
    if (not (order_by == '-last_seen')):
        raise ValueError(('Unsupported order_by: %s' % order_by))
    conditions = []
    if query:
        conditions.append(['tags_value', 'LIKE', '%{}%'.format(query)])
    (start, end) = self.get_time_range()
    results = snuba.query(start=start, end=end, groupby=['tags_value'], filter_keys={
        'project_id': [project_id],
        'environment': [environment_id],
        'tags_key': [key],
    }, aggregations=[['count()', '', 'times_seen'], ['min', 'timestamp', 'first_seen'], ['max', 'timestamp', 'last_seen']], conditions=conditions, orderby=order_by, limit=1000, referrer='tagstore.get_tag_value_paginator')
    tag_values = [TagValue(key=key, value=value, **fix_tag_value_data(data)) for (value, data) in six.iteritems(results)]
    desc = order_by.startswith('-')
    score_field = order_by.lstrip('-')
    return SequencePaginator([(int((to_timestamp(getattr(tv, score_field)) * 1000)), tv) for tv in tag_values], reverse=desc)