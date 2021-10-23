def get_tag_keys_for_projects(self, projects, environments, start, end, status=TagKeyStatus.VISIBLE):
    MAX_UNSAMPLED_PROJECTS = 50
    optimize_kwargs = {
        'turbo': True,
    }
    if (len(projects) <= MAX_UNSAMPLED_PROJECTS):
        optimize_kwargs['sample'] = 1
    return self.__get_tag_keys_for_projects(projects, None, environments, start, end, **optimize_kwargs)