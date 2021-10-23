def get_repo_choices(self, **kwargs):
    try:
        repos = self.get_repositories()
    except ApiError:
        repo_choices = []
    else:
        repo_choices = [(repo['identifier'], repo['name']) for repo in repos]
    params = kwargs.get('params', {
        
    })
    default_repo = params.get('repo', repo_choices[0][0])
    issues = self.get_repo_issues(default_repo)
    return (repo_choices, default_repo, issues)