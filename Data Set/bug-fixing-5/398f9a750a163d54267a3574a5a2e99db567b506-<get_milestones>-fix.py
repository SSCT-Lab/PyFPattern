def get_milestones(getter, project):
    url = 'https://api.github.com/repos/{project}/milestones'.format(project=project)
    data = getter.get(url)
    milestones = {
        
    }
    for ms in data:
        milestones[ms['title']] = ms['number']
    return milestones