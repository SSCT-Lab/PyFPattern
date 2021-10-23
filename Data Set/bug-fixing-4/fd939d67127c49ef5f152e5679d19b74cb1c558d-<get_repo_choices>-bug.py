def get_repo_choices(self, **kwargs):
    client = self.get_client()
    try:
        repos = client.get_repos(self.username)
    except ApiError:
        repo_choices = []
    else:
        repo_choices = [(repo['uuid'], repo['full_name']) for repo in repos['values']]
    params = kwargs.get('params', {
        
    })
    default_repo = params.get('repo', repo_choices[0][0])
    issues = self.get_repo_issues(default_repo)
    return (repo_choices, default_repo, issues)