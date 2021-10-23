def get_issues(getter, project, milestone):
    milestones = get_milestones(getter, project)
    mid = milestones[milestone]
    url = 'https://api.github.com/repos/{project}/issues?milestone={mid}&state=closed&sort=created&direction=asc'
    url = url.format(project=project, mid=mid)
    data = getter.get(url)
    issues = []
    for issue_data in data:
        issues.append(Issue(issue_data['number'], issue_data['title'], issue_data['html_url']))
    return issues