def get_milestones(getter, project):
    url = 'https://api.github.com/repos/{project}/milestones'.format(project=project)
    (raw_data, info) = getter.get(url)
    data = json.loads(raw_data)
    milestones = {
        
    }
    for ms in data:
        milestones[ms['title']] = ms['number']
    return milestones