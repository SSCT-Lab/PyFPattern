def get_group_tag_keys_and_top_values(self, project_id, group_id, environment_ids, user=None, keys=None, value_limit=TOP_VALUES_DEFAULT_LIMIT):
    (start, end) = self.get_time_range()
    keys_with_counts = self.get_group_tag_keys(project_id, group_id, environment_ids, keys=keys)
    filters = {
        'project_id': [project_id],
    }
    if environment_ids:
        filters['environment'] = environment_ids
    if (keys is not None):
        filters['tags_key'] = keys
    if (group_id is not None):
        filters['issue'] = [group_id]
    aggregations = [['count()', '', 'count'], ['min', SEEN_COLUMN, 'first_seen'], ['max', SEEN_COLUMN, 'last_seen']]
    values_by_key = snuba.query(start, end, ['tags_key', 'tags_value'], None, filters, aggregations, orderby='-count', limitby=[value_limit, 'tags_key'], referrer='tagstore.__get_tag_keys_and_top_values')
    if (group_id is None):
        value_ctor = TagValue
    else:
        value_ctor = functools.partial(GroupTagValue, group_id=group_id)
    for keyobj in keys_with_counts:
        key = keyobj.key
        values = values_by_key.get(key, [])
        keyobj.top_values = [value_ctor(key=keyobj.key, value=value, times_seen=data['count'], first_seen=parse_datetime(data['first_seen']), last_seen=parse_datetime(data['last_seen'])) for (value, data) in six.iteritems(values)]
    return keys_with_counts