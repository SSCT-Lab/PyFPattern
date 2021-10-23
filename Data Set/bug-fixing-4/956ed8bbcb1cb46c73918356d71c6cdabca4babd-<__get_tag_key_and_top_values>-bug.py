def __get_tag_key_and_top_values(self, project_id, group_id, environment_id, key, limit=3, raise_on_empty=True):
    (start, end) = self.get_time_range()
    tag = 'tags[{}]'.format(key)
    filters = {
        'project_id': [project_id],
        'environment': [environment_id],
    }
    if (group_id is not None):
        filters['issue'] = [group_id]
    conditions = [[tag, '!=', '']]
    aggregations = [['uniq', tag, 'values_seen'], ['count()', '', 'count'], ['min', SEEN_COLUMN, 'first_seen'], ['max', SEEN_COLUMN, 'last_seen']]
    (result, totals) = snuba.query(start, end, [tag], conditions, filters, aggregations, limit=limit, totals=True, referrer='tagstore.__get_tag_key_and_top_values')
    if (raise_on_empty and ((result is None) or (totals['count'] == 0))):
        raise (TagKeyNotFound if (group_id is None) else GroupTagKeyNotFound)
    else:
        if (group_id is None):
            key_ctor = TagKey
            value_ctor = TagValue
        else:
            key_ctor = functools.partial(GroupTagKey, group_id=group_id)
            value_ctor = functools.partial(GroupTagValue, group_id=group_id)
        top_values = [value_ctor(key=key, value=value, times_seen=data['count'], first_seen=parse_datetime(data['first_seen']), last_seen=parse_datetime(data['last_seen'])) for (value, data) in six.iteritems(result)]
        return key_ctor(key=key, values_seen=totals['values_seen'], count=totals['count'], top_values=top_values)