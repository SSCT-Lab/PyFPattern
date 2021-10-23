def __get_tag_keys_for_projects(self, projects, group_id, environments, start, end, limit=1000, keys=None):
    filters = {
        'project_id': projects,
    }
    if environments:
        filters['environment'] = environments
    if (group_id is not None):
        filters['issue'] = [group_id]
    if (keys is not None):
        filters['tags_key'] = keys
    aggregations = [['uniq', 'tags_value', 'values_seen'], ['count()', '', 'count']]
    conditions = [['tags_key', 'NOT IN', self.EXCLUDE_TAG_KEYS]]
    result = snuba.query(start, end, ['tags_key'], conditions, filters, aggregations, limit=limit, orderby='-values_seen', referrer='tagstore.__get_tag_keys')
    if (group_id is None):
        ctor = TagKey
    else:
        ctor = functools.partial(GroupTagKey, group_id=group_id)
    return set([ctor(key=key, values_seen=data['values_seen'], count=data['count']) for (key, data) in six.iteritems(result) if data['values_seen']])