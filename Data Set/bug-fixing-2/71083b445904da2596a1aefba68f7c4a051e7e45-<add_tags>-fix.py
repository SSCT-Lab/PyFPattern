

def add_tags(self, group, tags):
    from sentry.models import TagValue, GroupTagValue
    project_id = group.project_id
    date = group.last_seen
    for tag_item in tags:
        if (len(tag_item) == 2):
            ((key, value), data) = (tag_item, None)
        else:
            (key, value, data) = tag_item
        buffer.incr(TagValue, {
            'times_seen': 1,
        }, {
            'project_id': project_id,
            'key': key,
            'value': value,
        }, {
            'last_seen': date,
            'data': data,
        })
        buffer.incr(GroupTagValue, {
            'times_seen': 1,
        }, {
            'group_id': group.id,
            'key': key,
            'value': value,
        }, {
            'last_seen': date,
        })
