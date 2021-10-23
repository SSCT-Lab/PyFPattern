def get_group_list_tag_value(self, project_id, group_ids, environment_id, key, value):
    (start, end) = self.get_time_range()
    tag = 'tags[{}]'.format(key)
    filters = {
        'project_id': [project_id],
        'environment': [environment_id],
        'issue': group_ids,
    }
    conditions = [[tag, '=', value]]
    aggregations = [['count()', '', 'times_seen'], ['min', SEEN_COLUMN, 'first_seen'], ['max', SEEN_COLUMN, 'last_seen']]
    result = snuba.query(start, end, ['issue'], conditions, filters, aggregations, referrer='tagstore.get_group_list_tag_value')
    return {issue: GroupTagValue(group_id=issue, key=key, value=value, **fix_tag_value_data(data)) for (issue, data) in six.iteritems(result)}