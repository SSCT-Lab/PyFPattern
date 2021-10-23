def get_create_issue_config(self, group, **kwargs):
    fields = super(GitHubIssueBasic, self).get_create_issue_config(group, **kwargs)
    try:
        repos = self.get_repositories()
    except ApiError:
        repo_choices = [(' ', ' ')]
    else:
        repo_choices = [(repo['identifier'], repo['name']) for repo in repos]
    params = kwargs.get('params', {
        
    })
    default_repo = params.get('repo', repo_choices[0][0])
    assignees = self.get_allowed_assignees(default_repo)
    return (([{
        'name': 'repo',
        'label': 'GitHub Repository',
        'type': 'select',
        'default': default_repo,
        'choices': repo_choices,
        'updatesForm': True,
    }] + fields) + [{
        'name': 'assignee',
        'label': 'Assignee',
        'default': '',
        'type': 'select',
        'required': False,
        'choices': assignees,
    }])