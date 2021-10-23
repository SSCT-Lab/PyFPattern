def get_create_issue_config(self, group, **kwargs):
    '\n        These fields are used to render a form for the user,\n        and are then passed in the format of:\n\n        >>>{\'title\': \'TypeError: Object [object Object] has no method "updateFrom"\'\'}\n\n        to `create_issue`, which handles creation of the issue\n        in JIRA, VSTS, Github, etc\n        '
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