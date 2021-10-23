def get_issues(getter, project, milestone):
    milestones = get_milestones(getter, project)
    mid = milestones[milestone]
    url = 'https://api.github.com/repos/{project}/issues?milestone={mid}&state=closed&sort=created&direction=asc'
    url = url.format(project=project, mid=mid)
    raw_datas = []
    while True:
        (raw_data, info) = getter.get(url)
        raw_datas.append(raw_data)
        if ('link' not in info):
            break
        m = re.search('<(.*?)>; rel="next"', info['link'])
        if m:
            url = m.group(1)
            continue
        break
    issues = []
    for raw_data in raw_datas:
        data = json.loads(raw_data)
        for issue_data in data:
            issues.append(Issue(issue_data['number'], issue_data['title'], issue_data['html_url']))
    return issues