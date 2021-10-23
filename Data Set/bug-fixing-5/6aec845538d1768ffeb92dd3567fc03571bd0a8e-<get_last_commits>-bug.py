def get_last_commits(self, project_id, end_sha):
    "Get the last set of commits ending at end_sha\n\n        Gitlab doesn't give us a good way to do this, so we fetch the end_sha\n        and use its date to find the block of commits. We only fetch one page\n        of commits to match other implementations (github, bitbucket)\n\n        See https://docs.gitlab.com/ee/api/commits.html#get-the-diff-of-a-commit\n        "
    path = GitLabApiClientPath.commit.format(project=project_id, sha=end_sha)
    commit = self.get(path)
    if (not commit):
        return []
    end_date = commit['created_at']
    path = GitLabApiClientPath.commits.format(project=project_id)
    return self.get(path, params={
        'until': end_date,
    })