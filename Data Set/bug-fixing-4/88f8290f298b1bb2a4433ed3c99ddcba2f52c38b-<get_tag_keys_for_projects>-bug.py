def get_tag_keys_for_projects(self, projects, environments, start, end, status=TagKeyStatus.VISIBLE):
    return self.__get_tag_keys_for_projects(projects, None, environments, start, end)