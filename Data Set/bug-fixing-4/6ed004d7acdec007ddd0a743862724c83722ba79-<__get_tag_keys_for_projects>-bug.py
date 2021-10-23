def __get_tag_keys_for_projects(self, projects, group_id, environments, start, end, limit=1000, keys=None, include_values_seen=True, **kwargs):
    filters = {
        'project_id': projects,
    }
    if environments:
        filters['environment'] = environments
    if (group_id is not None):
        filters['group_id'] = [group_id]
    if (keys is not None):
        filters['tags_key'] = keys
    aggregations = [['count()', '', 'count']]
    if include_values_seen:
        aggregations.append(['uniq', 'tags_value', 'values_seen'])
    conditions = [['tags_key', 'NOT IN', self.EXCLUDE_TAG_KEYS]]
    result = snuba.query(start=start, end=end, groupby=['tags_key'], conditions=conditions, filter_keys=filters, aggregations=aggregations, limit=limit, orderby='-count', referrer='tagstore.__get_tag_keys', **kwargs)
    if (group_id is None):
        ctor = TagKey
    else:
        ctor = functools.partial(GroupTagKey, group_id=group_id)
    results = set()
    for (key, data) in six.iteritems(result):
        params = {
            'key': key,
        }
        if include_values_seen:
            params['values_seen'] = data['values_seen']
            params['count'] = data['count']
        else:
            params['count'] = data
        results.add(ctor(**params))
    return results