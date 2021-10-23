

def get_link_issue_config(self, group, **kwargs):
    (default_repo, repo_choices) = self.get_repository_choices(group, **kwargs)
    org = group.organization
    autocomplete_url = reverse('sentry-extensions-github-search', args=[org.slug, self.model.id])
    return [{
        'name': 'repo',
        'label': 'GitHub Repository',
        'type': 'select',
        'default': default_repo,
        'choices': repo_choices,
        'url': autocomplete_url,
        'required': True,
        'updatesForm': True,
    }, {
        'name': 'externalIssue',
        'label': 'Issue',
        'default': '',
        'type': 'select',
        'url': autocomplete_url,
        'required': True,
    }, {
        'name': 'comment',
        'label': 'Comment',
        'default': 'Sentry issue: [{issue_id}]({url})'.format(url=absolute_uri(group.get_absolute_url()), issue_id=group.qualified_short_id),
        'type': 'textarea',
        'required': False,
        'help': "Leave blank if you don't want to add a comment to the GitHub issue.",
    }]
