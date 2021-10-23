def __get_tag_value(self, project_id, group_id, environment_id, key, value):
    (start, end) = self.get_time_range()
    tag = 'tags[{}]'.format(key)
    filters = {
        'project_id': [project_id],
        'environment': [environment_id],
    }
    if (group_id is not None):
        filters['issue'] = [group_id]
    conditions = [[tag, '=', value]]
    aggregations = [['count()', '', 'times_seen'], ['min', SEEN_COLUMN, 'first_seen'], ['max', SEEN_COLUMN, 'last_seen']]
    data = snuba.query(start, end, [], conditions, filters, aggregations, referrer='tagstore.__get_tag_value')
    if (not (data['times_seen'] > 0)):
        raise (TagValueNotFound if (group_id is None) else GroupTagValueNotFound)
    else:
        data.update({
            'key': key,
            'value': value,
        })
        if (group_id is None):
            return TagValue(**fix_tag_value_data(data))
        else:
            return GroupTagValue(group_id=group_id, **fix_tag_value_data(data))