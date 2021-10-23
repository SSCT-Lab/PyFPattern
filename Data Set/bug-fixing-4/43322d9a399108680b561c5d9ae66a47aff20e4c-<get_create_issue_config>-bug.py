def get_create_issue_config(self, group, **kwargs):
    event = group.get_latest_event()
    if (event is not None):
        Event.objects.bind_nodes([event], 'data')
    return [{
        'name': 'title',
        'label': 'Title',
        'default': self.get_group_title(group, event, **kwargs),
        'type': 'string',
    }, {
        'name': 'description',
        'label': 'Description',
        'default': self.get_group_description(group, event, **kwargs),
        'type': 'textarea',
    }]