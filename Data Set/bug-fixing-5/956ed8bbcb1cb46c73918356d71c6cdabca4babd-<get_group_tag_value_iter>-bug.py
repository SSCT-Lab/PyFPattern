def get_group_tag_value_iter(self, project_id, group_id, environment_id, key, callbacks=()):
    (start, end) = self.get_time_range()
    results = snuba.query(start=start, end=end, groupby=['tags_value'], filter_keys={
        'project_id': [project_id],
        'environment': [environment_id],
        'tags_key': [key],
        'issue': [group_id],
    }, aggregations=[['count()', '', 'times_seen'], ['min', 'timestamp', 'first_seen'], ['max', 'timestamp', 'last_seen']], orderby='-first_seen', limit=1000)
    group_tag_values = [GroupTagValue(group_id=group_id, key=key, value=value, **fix_tag_value_data(data)) for (value, data) in six.iteritems(results)]
    for cb in callbacks:
        cb(group_tag_values)
    return group_tag_values