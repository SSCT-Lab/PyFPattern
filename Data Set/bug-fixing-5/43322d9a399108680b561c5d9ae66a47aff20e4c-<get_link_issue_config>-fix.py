def get_link_issue_config(self, group, **kwargs):
    '\n        Used by the `GroupIntegrationDetailsEndpoint` to\n        create an `ExternalIssue` using title/description\n        obtained from calling `get_issue` described below.\n        '
    return [{
        'name': 'externalIssue',
        'label': 'Issue',
        'default': '',
        'type': 'string',
    }]