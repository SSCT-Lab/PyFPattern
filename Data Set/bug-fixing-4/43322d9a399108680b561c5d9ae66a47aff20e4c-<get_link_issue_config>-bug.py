def get_link_issue_config(self, group, **kwargs):
    return [{
        'name': 'externalIssue',
        'label': 'Issue',
        'default': '',
        'type': 'string',
    }]