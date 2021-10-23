def get_link_issue_config(self, group, **kwargs):
    try:
        repos = self.get_repositories()
    except ApiError:
        repo_choices = [(' ', ' ')]
    else:
        repo_choices = [(repo['full_name'], repo['full_name']) for repo in repos]
    params = kwargs.get('params', {
        
    })
    default_repo = params.get('repo', repo_choices[0][0])
    issues = self.get_repo_issues(default_repo)
    return [{
        'name': 'repo',
        'label': 'GitHub Repository',
        'type': 'select',
        'default': default_repo,
        'choices': repo_choices,
        'updatesForm': True,
    }, {
        'name': 'externalIssue',
        'label': 'Issue',
        'default': '',
        'type': 'select',
        'choices': issues,
    }, {
        'name': 'comment',
        'label': 'Comment',
        'default': '',
        'type': 'textarea',
        'required': False,
        'help': "Leave blank if you don't want to add a comment to the GitHub issue.",
    }]